#!/usr/bin/env python3

import os
import sys

from glob import iglob
from dry import metadata, lang_name


def get_ext(file):
    return os.path.splitext(file)[1].lower().lstrip('.')

def get_lang(exts):
    for ext in exts:
        if ext in lang_name:
            return lang_name[ext]


if len(sys.argv) != 2:
    exit('usage: ./make_users.py [year]')
year = int(sys.argv[1])


langs = []
for contest in metadata[year]:
    for problem in contest['problems']:
        for directory in iglob('../source/{}/*'.format(problem['id'])):
            io, name = os.path.split(directory)[1].split('-')
            exts = {get_ext(file) for file in iglob('{}/*'.format(directory))}
            lang = get_lang(exts)
            if lang is not None:
                uid = '(SELECT id FROM users WHERE name = "{}")'.format(name)
                langs += [(lang, problem['id'], io, uid)]

for lang, pid, io, uid in langs:
    print('UPDATE answers SET lang = "{}"'.format(lang), end=' ')
    print('WHERE problem_id = {}'.format(pid), end=' ')
    print('AND hardness = {}'.format(io), end=' ')
    print('AND user_id = {}'.format(uid), end='')
    print(';')
