import os
import re
import yaml
import enchant
from collections import Counter

from framework._utils import datapath


_LANG_DICT = {}


class Identifier(str):

    english_dictionary = enchant.Dict('en_US')
    re_word_spec = re.compile(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|[0-9]|$)')

    @classmethod
    def _readable(cls, word):
        return len(word) > 1 and cls.english_dictionary.check(word)

    def _split_words(self):
        return self.re_word_spec.findall(self)

    def readable(self):
        return all(self._readable(word) for word in self._split_words())


class WordProcessor(object):

    def __init__(self, name, quoting=None, line_comment=None,
                 block_comment=None, keywords=None,
                 noise=r'[^a-zA-Z_0-9]', numeric=r'\b[0-9]+[ejl]?\b',
                 std_functions=None, lib_functions=None, **_):
        self.name = name
        self.re_quoting = re.compile(quoting, flags=re.DOTALL)
        self.re_line_comment = re.compile(line_comment)
        self.re_block_comment = None and re.compile(block_comment, flags=re.DOTALL)
        self.re_keywords = re.compile(r'\b(' + '|'.join(keywords) + r')\b')
        self.re_noise = re.compile(noise)
        self.re_numeric = re.compile(numeric)
        self.std_functions = std_functions
        self.lib_functions = lib_functions

    def extract_libraries(self, sourcecode):
        pass

    def strip_string(self, sourcecode):
        return self.re_quoting.sub(' ', sourcecode)

    def strip_comment(self, sourcecode):
        if self.re_block_comment is not None:
            sourcecode = self.re_block_comment.sub(' ', sourcecode)
        return self.re_line_comment.sub(' ', sourcecode)

    def strip_keywords(self, sourcecode):
        return self.re_keywords.sub(' ', sourcecode)

    def strip_noise(self, sourcecode):
        return self.re_noise.sub(' ', sourcecode)

    def strip_numeric(self, sourcecode):
        return self.re_numeric.sub(' ', sourcecode)

    def get_variable_names(self, sourcecode):
        intercode = self.strip_string(sourcecode)
        intercode = self.strip_comment(intercode)
        intercode = self.strip_keywords(intercode)
        intercode = self.strip_noise(intercode)
        intercode = self.strip_numeric(intercode)
        return Counter(intercode.split())

    def get_line_of_blocks(self, sourcecode):
        if self.name == 'Python':
            return self._python_line_of_blocks(sourcecode)
        elif self.name in ['Java', 'C#']:
            return self._java_line_of_blocks(sourcecode)
        else:
            return self._cpp_line_of_blocks(sourcecode)

    def _python_line_of_blocks(self, sourcecode):
        lines = sourcecode.splitlines()
        in_block = False
        blocks = []
        for index, line in enumerate(lines):
            if line.startswith(' ') or line.startswith('\t'):
                if not in_block:
                    while True:
                        index -= 1
                        block_name = lines[index].strip()
                        if block_name:
                            break
                    blocks += [[block_name, 1]]
                in_block = True
            elif line.strip():
                if in_block:
                    while not lines[index-1].strip():
                        index -= 1
                        blocks[-1][1] -= 1
                in_block = False
            if in_block:
                blocks[-1][1] += 1
        return blocks

    def _cpp_line_of_blocks(self, sourcecode):
        sourcecode = self.strip_string(sourcecode)
        sourcecode = self.strip_comment(sourcecode)
        sym_open = '{'
        sym_close = '}'
        depth = 0
        blocks = []
        for index, char in enumerate(sourcecode):
            if char == sym_open:
                if depth == 0:
                    before = index
                    while True:
                        before = max(0, sourcecode.rfind('\n', 0, before))
                        block_name = sourcecode[before:index].strip()
                        if block_name or before == 0:
                            break
                    blocks += [[block_name, 0]]
                depth += 1
            elif char == sym_close:
                depth -= 1
            if depth > 0 and char == '\n':
                blocks[-1][1] += 1
        return [[it, length] for it, length in blocks if it.find('=') == -1]

    def _java_line_of_blocks(self, sourcecode):
        sourcecode = self.strip_string(sourcecode)
        sourcecode = self.strip_comment(sourcecode)
        sym_open = '{'
        sym_close = '}'
        depth = 0
        blocks = []
        for index, char in enumerate(sourcecode):
            if char == sym_open:
                if depth == 1:
                    before = index
                    while True:
                        before = max(0, sourcecode.rfind('\n', 0, before))
                        block_name = sourcecode[before:index].strip()
                        if block_name:
                            break
                    blocks += [[block_name, 0]]
                depth += 1
            elif char == sym_close:
                depth -= 1
            if depth > 1 and char == '\n':
                blocks[-1][1] += 1
        return [[it, length] for it, length in blocks if it.find('=') == -1]


def _lazy_init():
    if not _LANG_DICT:
        directory = datapath('_config', 'language')
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            language_spec = yaml.load(open(filepath))
            source_processor = WordProcessor(**language_spec)
            for extension in language_spec['extensions']:
                _LANG_DICT['.'+extension] = source_processor


def determine_languages(directory):
    _lazy_init()
    used_languages = set()
    for filename in os.listdir(directory):
        _, ext = os.path.splitext(filename)
        if ext in _LANG_DICT:
            used_languages |= {_LANG_DICT[ext].name}
    return used_languages


def select(ext):
    _lazy_init()
    return _LANG_DICT[ext.lower()]
