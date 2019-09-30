import json
from psaw import PushshiftAPI

from reddit_auth import reddit

api = PushshiftAPI()

BEFORE_CREATED_UTC = None

def parse_bestof(bestof_submission):
    out = {}
    out['bestof_created_utc'] = bestof_submission.created_utc
    url_ = bestof_submission.url.split('?')
    url = url_[0].split('/')
    url_params = None
    if len(url_) > 1:
        url_params = url_[1]
    try:
        submission_id = url[6]
        comment_id = None
        if len(url) >= 9:
            comment_id = url[8]
        target_id = comment_id if comment_id else submission_id
        target = target_id + ' ' + bestof_submission.title
        out['target'] = target
    except:
        return
    # generate input data
    subtext = ['submission']
    submission = reddit.submission(submission_id)
    try:
        if submission.author:
            subtext.append('u/' + submission.author.name)
        else:
            subtext.append('[deleted]')
    except:
        return
    out['subreddit'] = submission.subreddit.display_name
    subtext.append(submission.title)
    if submission.is_self:
        subtext.append(submission.selftext)
    else:
        subtext.append(submission.url)
    subtext.append(submission_id)
    comments = submission.comments.list()
    for comment in comments:
        # the other alternative is MoreComments
        if comment.__class__.__name__ == 'Comment':
            # ignore comments after r/bestof submission
            too_late = comment.created_utc >= bestof_submission.created_utc
            # comments with score < 3 are definitely not r/bestof material
            low_score = comment.score < 3
            if low_score or too_late: continue
            if comment.created_utc < bestof_submission.created_utc:
                parent_id = comment.parent_id.split('_')[1]
                if parent_id == submission_id:
                    subtext.append('top-level')
                else:
                    subtext.append('reply')
                subtext.append(parent_id)
                if comment.author:
                    subtext.append('u/' + comment.author.name)
                else:
                    subtext.append('[deleted]')
                subtext.append(comment.body)
                subtext.append(comment.id)
    out['input'] = '\n'.join(subtext)
    return out

if __name__== '__main__':
    params = {
        'subreddit': 'bestof',
        'filter': ['id', 'title', 'created_utc', 'url', 'subreddit', 'score'],
        'sort_type': 'created_utc',  # default
        'sort': 'desc'  # default
    }
    if BEFORE_CREATED_UTC is not None:
        params['before'] = BEFORE_CREATED_UTC
    n = 0
    for bestof_submission in api.search_submissions(**params):
        n+=1
        if bestof_submission.score < 3:
            # There's a surprising amount of garbage on r/bestof
            continue
        if bestof_submission.subreddit != 'bestof':
            break
        if n == 10000:
            break
        out = parse_bestof(bestof_submission)
        if out: print(json.dumps(out))
