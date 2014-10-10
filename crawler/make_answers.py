#!/usr/bin/env python3

import os
import sys
import json
import yaml

def iter_id_io(problems):
    for problem in problems:
        c = 0
        while c < problem['io']:
            yield problem['id'], c
            c += 1


if len(sys.argv) != 2:
    exit('usage: ./make_users.py [year]')
year = int(sys.argv[1])

metadata = yaml.load(open('metadata.yaml').read())

base = set()
more = set()
for contest in metadata[year]:
    adaptor = base if 'Qualification' in contest['name'] else more
    for user in json.load(open(filename)):
        adaptor.add(user['n'])
if more - base:
    raise NameError(more - base)

answers = []
for contest in metadata[year]:
    filename = 'data/{}.json'.format(contest['id'])
    if not os.path.isfile(filename):
        exit('data for year {} does not exist.'.format(year))
    for answer in json.load(open(filename)):
        us = '(SELECT id FROM users WHERE name = {n!r})'.format(**answer)
        id_io = iter_id_io(contest['problems'])
        for a, s, o, (num, io) in zip(answer['att'], answer['ss'], answer['oa'], id_io):
            if a == 0:
                continue
            answers += ['  ({}, {}, {}, {}, {})'.format(us, num, io, a, s)]

print('INSERT INTO answers (user_id, problem_id, hardness, attempts, submit_time)\nVALUES')
print(',\n'.join(answers))
print(';')
