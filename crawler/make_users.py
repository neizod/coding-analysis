#!/usr/bin/env python3

import os
import sys
import json

from dry import metadata


if len(sys.argv) != 2:
    exit('usage: ./make_users.py [year]')
year = int(sys.argv[1])


contest = next(c for c in metadata[year] if 'Qualification' in c['name'])
filename = 'data/{}.json'.format(contest['id'])
if not os.path.isfile(filename):
    exit('data for year {} does not exist.'.format(year))

users = ['  ({n!r}, {c!r})'.format(**u) for u in json.load(open(filename))]
print('INSERT INTO users (name, country)\nVALUES')
print(',\n'.join(users))
print(';')
