from reddit_auth import reddit
import wordpress


def write_wordpress_post(comment):
    title = comment.submission.title
    if '?' not in title: return 'Not a question. Did not post.'
    try:
        if comment.author:
            author = 'u/' + comment.author.name
        else:
            author = '[deleted]'
    except:
        return 'No author found. Did not post'
    url = 'https://www.reddit.com' + comment.permalink + '?context=1000'
    wp_post = {}
    wp_post['title'] = f'Reddit Gold: "{title}"'
    opening_blurb = (
        f'<i>Reddit Gold</i> highlights the most useful and educational content '
        f'on Reddit as found on <a href="https://www.reddit.com/r/AutoBestOf/">r/AutoBestOf</a>. '
        f'\n\n'
        f'Today\'s post is from <strong>{author}</strong> who answers the question: "<i>{title}</i>"'
    )
    wp_post['content'] = (
        f'{opening_blurb}'
        f'\n'
        f'<blockquote cite="{url}">{comment.body_html}</blockquote>'
        f'<a href="{url}">Source</a>'
    )
    resp = wordpress.create_post(wp_post)
    return resp.status_code


if __name__== '__main__':
    r_autobestof = reddit.subreddit('autobestof')
    wp_posts = [post['title']['rendered'] for post in wordpress.get_posts()]
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
        else:
            curr_title = comment.submission.title
            title_matches = [curr_title in existing_title for existing_title in wp_posts]
            if not any(title_matches): print(write_wordpress_post(comment))
