#!/usr/bin/env python3

import os
import sys
import json
import urllib3
from itertools import count

from codejam_header import metadata


if len(sys.argv) != 2:
    exit('usage: {} [year]'.format(__file__))
year = int(sys.argv[1])

http = urllib3.PoolManager()

api = metadata['api']
default = {'cmd': 'GetScoreboard', 'show_type': 'all'}

os.makedirs('../data', exist_ok=True)
for contest in metadata[year]:
    filename = '../data/{}.json'.format(contest['id'])
    if os.path.isfile(filename):
        continue
    print('{}'.format(contest['id']), end=''); sys.stdout.flush()
    default['contest_id'] = contest['id']
    contest_stat = []
    for i in count(1, 30):
        default['start_pos'] = i
        result = http.request('GET', api, fields=default)
        data = json.loads(result.data.decode('utf-8'))
        contest_stat += data['rows']
        print('.', end=''); sys.stdout.flush()
        if i + 30 > data['stat']['nrp']:
            break
    with open(filename, 'w') as file:
        json.dump(contest_stat, file)
    print()
