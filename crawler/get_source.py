#!/usr/bin/env python3

import os
import sys
import json
import yaml
import urllib3
from itertools import count

def exist_source(attempt, submittime):
    if not attempt or submittime == -1:
        return False
    return True

def iter_id_io(problems):
    for problem in problems:
        c = 0
        while c < problem['io']:
            yield problem['id'], c
            c += 1

if len(sys.argv) != 2:
    exit('usage: ./get_source.py [year]')
year = int(sys.argv[1])

metadata = yaml.load(open('metadata.yaml').read())
http = urllib3.PoolManager()

api = metadata['api']
default = {'cmd': 'GetSourceCode'}

os.makedirs('source', exist_ok=True)
for contest in metadata[year]:
    filename = 'data/{}.json'.format(contest['id'])
    if not os.path.isfile(filename):
        exit('data for year {} does not exist.'.format(year))
    default['contest'] = contest['id']
    for answer in json.load(open(filename)):
        name = answer['n']
        print(name, '', end=''); sys.stdout.flush()
        id_io = iter_id_io(contest['problems'])
        for a, s, o, (num, io) in zip(answer['att'], answer['ss'], answer['oa'], id_io):
            if not exist_source(a, s):
                continue
            sourcezip = 'source/{}-{}-{}.zip'.format(num, io, answer['n'])
            if os.path.isfile(sourcezip):
                continue
            default['problem'] = num
            default['io_set_id'] = io
            default['username'] = name
            result = http.request('GET', api, fields=default)
            with open(sourcezip, 'wb') as file:
                file.write(result.data)
            print('.', end=''); sys.stdout.flush()
        print()
