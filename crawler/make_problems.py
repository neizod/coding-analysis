#!/usr/bin/env python3

import os
import sys
import json
import yaml

if len(sys.argv) != 2:
    exit('usage: ./make_problems.py [year]')
year = int(sys.argv[1])

metadata = yaml.load(open('metadata.yaml').read())

problems = []
for contest in metadata[year]:
    for problem in contest['problems']:
        problems += ['  ({id}, {name!r})'.format(**problem)]

print('INSERT INTO problems (id, name)\nVALUES')
print(',\n'.join(problems), end='')
print(';')
