import pandas as pd

from reddit_auth import reddit

def get_subreddit(target_id):
    try:
        try:
            comment = reddit.comment(target_id)
            submission = comment.submission
        except:
            submission = reddit.submission(target_id)
        return submission.subreddit
    except:
        return None

rbestof = pd.read_json('rbestof.json', orient='records', lines=True)['target']
ids_ = rbestof.str.split(' ').str[0]
subreddits = ids_.apply(get_subreddit)

# import json
# n = 0
# with open('rbestof.json') as f:
#     for line in f:
#         try:
#             json_obj = json.loads(line)
#         except:
#             n += 1
#             print(line)
#     print(f'{n} fucked up lines')
