#!/usr/bin/env python3

import os
import sys
import json

from glob import iglob
from dry import metadata, lang_name, iter_id_io


def get_ext(file):
    return os.path.splitext(file)[1].lower().lstrip('.')

def get_lang(exts):
    for ext in exts:
        if ext in lang_name:
            return lang_name[ext]


if not 2 < len(sys.argv) <= 3:
    exit('usage: ./make_users.py [year] [contest]')
year = int(sys.argv[1])
cont = sys.argv[2] if sys.argv[2] else None


base = set()
more = set()
for contest in metadata[year]:
    adaptor = base if 'Qualification' in contest['name'] else more
    for user in json.load(open('../data/{}.json'.format(contest['id']))):
        adaptor.add(user['n'])
if more - base:
    raise NameError(more - base)

answers = []
for contest in metadata[year]:
    if cont is not None and cont.lower() not in contest['name'].lower():
        continue
    filename = '../data/{}.json'.format(contest['id'])
    if not os.path.isfile(filename):
        exit('data for year {} does not exist.'.format(year))
    for answer in json.load(open(filename)):
        us = '(SELECT id FROM users WHERE name = {n!r})'.format(**answer)
        id_io = iter_id_io(contest['problems'])
        for a, s, o, (num, io) in zip(answer['att'], answer['ss'], answer['oa'], id_io):
            if a == 0:
                continue
            if s != -1:
                files = '../source/{}/{}-{}/*'.format(num, io, answer['n'])
                exts = {get_ext(file) for file in iglob(files)}
                lang = get_lang(exts)
            else:
                s = None
                lang = None
            answers += ['  ({}, {}, {}, {}, {}, {!r})'.format(us, num, io, a, s, lang)]

print('INSERT INTO answers (user_id, problem_id, hardness, attempts, submit_time, lang)\nVALUES')
print(',\n'.join(answers))
print(';')
