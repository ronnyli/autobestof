import pickle

from reddit_auth import reddit
import stream

with open('model.pkl', 'rb') as f:
    clf = pickle.load(f)

if __name__== '__main__':
    r_autobestof = reddit.subreddit('autobestof')
    comments = []
    for comment in stream.stream_all_comments(reddit):
        comments.append(comment)
        if len(comments) > 1000:
            txt = [c.body for c in comments]
            pred = clf.predict_proba(txt)[:, 1]
            top_cmt = comments[pred.argmax()]
            comments = []
            top_sub = top_cmt.submission
            cmt_url = 'www.reddit.com' + top_sub.permalink + top_cmt.id + '?context=1000'
            r_autobestof.submit(title=top_sub.title, url=cmt_url)
            print(top_cmt.body)
    # submissions = []
    # for submission in reddit.subreddit('all').stream.submissions():
    #     if submission.selftext != '' and not submission.over_18:
    #         submissions.append(submission)
    #     if len(submissions) > 100:
    #         txt = [s.selftext for s in submissions]
    #         pred = clf.predict_proba(txt)[:, 1]
    #         top_sub = submissions[pred.argmax()]
    #         submissions = []
    #         r_autobestof.submit(title=top_sub.title, url=top_sub.url)
    #         print(top_sub.selftext)
