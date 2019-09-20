from collections import OrderedDict
import math
import pickle

from reddit_auth import reddit
import stream

class LRU(OrderedDict):
    'Limit size, evicting the least recently looked-up key when full'

    def __init__(self, maxsize=128, *args, **kwds):
        self.maxsize = maxsize
        super().__init__(*args, **kwds)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if len(self) > self.maxsize:
            oldest = next(iter(self))
            del self[oldest]


if __name__== '__main__':
    comments = LRU(maxsize=2000000)  # 1 million entries
    r_autobestof = reddit.subreddit('autobestof')
    for comment in stream.stream_all_comments(reddit):
        # stream all comments for instances of thanks
        body = comment.body.lower()
        if ('thank you' in body) \
            and comment.parent_id.startswith('t1_'):
            # record their parent_ids
            try:
                comments[comment.parent_id] += 1
                if comments[comment.parent_id] == 4:
                    print(comment.body)
                    # when a parent_id hits X then post it to r/autobestof
                    # (make sure parent_ids that were already posted don't get posted again)
                    parent_id = comment.parent_id.split('_')[1]
                    parent_comment = reddit.comment(parent_id)
                    if math.log(len(parent_comment.body)) > 3:
                        # check log(length) of parent_id post
                        r_autobestof.submit(
                            title=parent_comment.submission.title,
                            url='www.reddit.com' + parent_comment.permalink + '?context=1000')
                        print(parent_comment.permalink)
                        print(parent_comment.body)
            except KeyError:
                print(comment.parent_id)
                comments[comment.parent_id] = 1
        # remove old parent_ids (already handled by LRU)