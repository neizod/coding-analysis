#!/usr/bin/env python3

import sys
import json
import urllib3
from itertools import count

import dry


if len(sys.argv) != 2:
    exit('usage: {} [year]'.format(__file__))
year = int(sys.argv[1])

http = urllib3.PoolManager()

api = dry.metadata['api']
default = {'cmd': 'GetScoreboard', 'show_type': 'all'}

dry.makedirs('metadata')
for contest in dry.metadata[year]:
    filename = 'metadata/round/{}.json'.format(contest['id'])
    if dry.isfile(filename):
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
    with dry.open(filename, 'w') as file:
        json.dump(contest_stat, file, sort_keys=True, indent=4)
    print()
