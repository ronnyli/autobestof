from reddit_auth import reddit

if __name__== '__main__':
    r_autobestof = reddit.subreddit('autobestof')
    for submission in r_autobestof.stream.submissions():
        sub_url = submission.url.split('/')
        link_id = sub_url[6]
        comment_id = sub_url[8]
        comment = reddit.comment(comment_id)
        # Replies don't appear unless you refresh
        # https://github.com/praw-dev/praw/issues/413#issuecomment-133202208
        comment.refresh()
        authors = {}
        for reply in comment.replies:
            # direct replies only
            try:
                if 'thank you' in reply.body.lower():
                    author = reply.author.name
                    try:
                        authors[author] += 1
                    except KeyError:
                        authors[author] = 1
            except AttributeError:
                pass
        if len(authors) < 3:
            print(submission.url)
            submission.delete()
