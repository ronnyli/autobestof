from reddit_auth import reddit
from prawcore.exceptions import ResponseException, RequestException, ServerError


if __name__== '__main__':
    r_autobestof = reddit.subreddit('autobestof')
    while True:
        try:
            for submission in r_autobestof.stream.submissions():
                comments = submission.comments.list()
                if len(comments) > 0:
                    comment_from_me = [c.author.name == 'sirius_li' for c in comments]
                    if any(comment_from_me):
                        # autobestof_cleanup already ran on this submission
                        continue
                sub_url = submission.url.split('/')
                link_id = sub_url[6]
                comment_id = sub_url[8]
                comment = reddit.comment(comment_id)
                # Replies don't appear unless you refresh
                # https://github.com/praw-dev/praw/issues/413#issuecomment-133202208
                try:
                    comment.refresh()
                except:
                    # something happened to the comment to make it inaccessible
                    # i.e., subreddit quarantined, set to private, etc
                    submission.delete()
                    continue
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
        except (ResponseException, RequestException, ServerError) as e:
            print(e)
            time.sleep(60)
            continue
        except:
            raise
