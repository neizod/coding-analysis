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
default = {'cmd': 'GetSourceCode'}

dry.makedirs('sourcezip')
for contest in dry.metadata[year]:
    filename = 'metadata/round/{}.json'.format(contest['id'])
    if not dry.isfile(filename):
        exit('data for year {} does not exist.'.format(year))
    default['contest'] = contest['id']
    for answer in json.load(open(filename)):
        name = answer['n']
        print(name, '', end=''); sys.stdout.flush()
        id_io = dry.iter_id_io(contest['problems'])
        for a, s, o, (num, io) in zip(answer['att'], answer['ss'], answer['oa'], id_io):
            if not dry.exist_source(a, s):
                continue
            sourcezip = 'sourcezip/{}-{}-{}.zip'.format(num, io, answer['n'])
            if dry.isfile(sourcezip):
                continue
            default['problem'] = num
            default['io_set_id'] = io
            default['username'] = name
            result = http.request('GET', api, fields=default)
            with dry.open(sourcezip, 'wb') as file:
                file.write(result.data)
            print('.', end=''); sys.stdout.flush()
        print()
