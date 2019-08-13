from reddit_auth import reddit
import stream

# for comment in stream.stream_all_comments(reddit):
#     print(comment.body)

if __name__== '__main__':
    r_autobestof = reddit.subreddit('autobestof')
    for submission in reddit.subreddit('all').stream.submissions():
        if submission.selftext != '' and not submission.over_18:
            print(submission.selftext)
            # r_autobestof.submit(title=submission.title, selftext=submission.selftext)
