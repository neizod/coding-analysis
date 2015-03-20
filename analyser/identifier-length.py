#!/usr/bin/env python3

import os
import codecs
import statistics as stat
from collections import Counter, defaultdict

import word_processor


identifier_length = defaultdict(list)
for file in open('../find-source.txt'):
    file = '../' + file.strip()
    _, ext = os.path.splitext(file)
    try:
        prolang = word_processor.select(ext)
    except KeyError:
        continue
    try:
        sourcecode = open(file).read()
    except UnicodeDecodeError:
        sourcecode = codecs.open(file, encoding='latin1').read()
    #identifier_length[prolang.name] += [len(identifier)]
    identifiers = prolang.get_variable_names(sourcecode)
    if not identifiers:
        continue
    mean = stat.mean(len(identifier) for identifier in identifiers)
    _, _, problem_id, hardness_username, _ = file.split('/')
    hardness, username = hardness_username.split('-')
    print(problem_id, hardness, username, mean, repr(prolang.name))


#for language, lengths in identifier_length.items():
#    print(language)
#    print(Counter(lengths))
#    print()
