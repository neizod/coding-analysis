#!/usr/bin/env python3

import os
import codecs
from collections import Counter, defaultdict

import word_processor


#words = defaultdict(Counter)
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
    for identifier, _ in prolang.get_variable_names(sourcecode).items():
        #if word_processor.Identifier.is_readable(identifier):
        #    words[prolang.name][identifier] += 1
        #else:
        #    words[prolang.name][identifier] -= 1
        identifier_length[prolang.name] += [len(identifier)]


#for language, counter in words.items():
#    print(language)
#    read = sum(c > 0 for c in counter.values())
#    what = sum(c < 0 for c in counter.values())
#    print(read/len(counter)*100, '%', '\t', '(', read, ':', what, ')', sep='')
#    print()
#
#for language, counter in words.items():
#    print(language, counter)
#    print()

for language, lengths in identifier_length.items():
    print(language)
    print(Counter(lengths))
    print()
