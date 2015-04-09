#!/usr/bin/env python3

import os
import sys
import codecs
from glob import iglob


def get_user(path):
    head, filename = os.path.split(path)
    head, io_name = os.path.split(head)
    io, name = io_name.split('-')
    return name

if len(sys.argv) != 2:
    exit('usage: ./cheat.py <problem_set>')

contents = {}
no_all_file = 0
for filename in iglob('../source/{}/*/*'.format(sys.argv[1])):
    with codecs.open(filename, 'r', encoding='latin1') as f:
        content = f.read()
        if content not in contents:
            contents[content] = []
            contents[content] += [filename]
        else:
            their_names = [get_user(name) for name in contents[content]]
            if get_user(filename) not in their_names:
                contents[content] += [filename]
    no_all_file += 1


cheaters = [names for names in contents.values() if len(names) > 1]
for names in cheaters: print(*names)
print('{}/{}'.format(len(cheaters), no_all_file))
