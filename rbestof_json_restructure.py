import json
import sys

for line in sys.stdin:
    # dict_keys(['bestof_created_utc', 'input', 'target'])
    rbestof = json.loads(line)
    print('<|startoftext|>')
    print(rbestof['input'])
    print('<|rbestof|>')
    print(rbestof['target'])
    print('<|endoftext|>')
