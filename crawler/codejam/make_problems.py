#!/usr/bin/env python3

import os
import sys
import json

from dry import metadata


if len(sys.argv) != 2:
    exit('usage: ./make_problems.py [year]')
year = int(sys.argv[1])

problems = []
for contest in metadata[year]:
    for problem in contest['problems']:
        problems += ['  ({id}, {name!r})'.format(**problem)]

print('INSERT INTO problems (id, name)\nVALUES')
print(',\n'.join(problems), end='')
print(';')
