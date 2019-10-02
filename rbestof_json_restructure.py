from gpt2_config import Gpt2Generator

import json
import re
import sys

gpt2 = Gpt2Generator()
gpt2.get_encoder()

def find_comment(target_id, txt):
    before_id = txt.split(target_id)[0]
    after_username = re.split('(u/\w+?)\\n', before_id)[-2:]
    return '\n'.join(after_username)

def restrict_length(all_txt, max_tokens=1023, output_len=30):
    '''Max length of document must be `max_tokens` long after the encoding step'''
    enc = gpt2.encoder
    input_txt = all_txt.pop(1)
    output_txt = all_txt.pop(2)
    output_tokens = enc.encode(output_txt)[:output_len]
    n_output = len(output_tokens)
    output_trunc = enc.decode(output_tokens)
    misc_txt = '\n'.join(all_txt)
    n_misc = len(enc.encode(misc_txt))
    n_input = max_tokens - n_output - n_misc
    assert n_input > 960, output_trunc + ' ' + misc_txt
    input_trunc = enc.decode(enc.encode(input_txt)[:n_input])
    all_txt.insert(2, output_trunc)
    all_txt.insert(1, input_trunc)
    return all_txt

for line in sys.stdin:
    # dict_keys(['bestof_created_utc', 'input', 'target'])
    rbestof = json.loads(line)
    target_id, target = rbestof['target'].split(maxsplit=1)
    comment_txt = find_comment(target_id, rbestof['input'])
    if len(comment_txt) == 0 or len(target) == 0: continue
    all_txt = ['<|startoftext|>', comment_txt, '<|rbestof|>', target, '<|endoftext|>']
    all_trunc = restrict_length(all_txt)
    for txt in all_trunc:
        print(txt)
