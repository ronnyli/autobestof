import gpt2_config
from reddit_auth import reddit
import wordpress


def write_wordpress_post(comment):
    title = comment.submission.title
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

class Gpt2Generator(object):
    def __init__(self, max_tokens=915):
        self.max_tokens = max_tokens
        self.encoder = gpt2_config.get_encoder()
        self.sess, self.gpt2 = gpt2_config.load_gpt2()

    def generate_titles(self, comment):
        try:
            author = comment.author.name
        except:
            author = 'u/Redditor'
        body_ = '\n'.join([author, comment.body])
        max_body_tokens = self.max_tokens - 15  # we will append more tokens
        body_trunc = self.encoder.decode(self.encoder.encode(body_)[:max_body_tokens])
        body = '\n'.join([body_trunc, comment.id, '<|rbestof|>'])
        titles = self.gpt2.generate(self.sess,
            length=100,
            temperature=0.7,
            prefix=body,
            nsamples=5,
            batch_size=5,
            include_prefix=False,
            truncate='<|endoftext|>',
            return_as_list=True
        )
        titles = [title.split(maxsplit=1)[1] for title in titles]
        return titles


if __name__== '__main__':
    r_autobestof = reddit.subreddit('autobestof')
    wp_posts = [post['title']['rendered'] for post in wordpress.get_posts()]
    gpt2 = Gpt2Generator()
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
            # Post to WP
            curr_title = comment.submission.title
            title_matches = [curr_title in existing_title for existing_title in wp_posts]
            if not any(title_matches): print(write_wordpress_post(comment))
            # GPT2 Titles
            generated_text = ['Auto-generated titles for this post (WIP)'] + gpt2.generate_titles(comment)
            submission.reply('\n'.join(generated_text))
