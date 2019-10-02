from gpt2_config import Gpt2Generator

import json
import re
import sys

def find_comment(target_id, txt):
    before_id = txt.split(target_id)[0]
    after_username = re.split('(u/\w+?)\\n', before_id)[-2:]
    return '\n'.join(after_username)

def restrict_length(txt, n_tokens=900):
    enc = encoder.get_encoder('checkpoint/run1/')
    return enc.decode(enc.encode(txt)[:n_tokens])

for line in sys.stdin:
    # dict_keys(['bestof_created_utc', 'input', 'target'])
    rbestof = json.loads(line)
    target_id, target = rbestof['target'].split(maxsplit=1)
    comment_txt = find_comment(target_id, rbestof['input'])
    comment_txt = restrict_length(comment_txt)
    if len(comment_txt) == 0 or len(rbestof['target']) == 0: continue
    print('<|startoftext|>')
    print(comment_txt)
    print('<|rbestof|>')
    print(target)
    print('<|endoftext|>')
