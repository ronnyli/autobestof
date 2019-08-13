import pickle

from reddit_auth import reddit

# import stream
# for comment in stream.stream_all_comments(reddit):
#     print(comment.body)

with open('model.pkl', 'rb') as f:
    clf = pickle.load(f)

if __name__== '__main__':
    r_autobestof = reddit.subreddit('autobestof')
    submissions = []
    for submission in reddit.subreddit('all').stream.submissions():
        if submission.selftext != '' and not submission.over_18:
            submissions.append(submission)
        if len(submissions) > 100:
            txt = [s.selftext for s in submissions]
            pred = clf.predict_proba(txt)[:, 1]
            top_sub = submissions[pred.argmax()]
            submissions = []
            r_autobestof.submit(title=top_sub.title, url=top_sub.url)
