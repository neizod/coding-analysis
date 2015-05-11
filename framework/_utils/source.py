import os
import re
import yaml
import enchant
from collections import Counter

from framework._utils import LazyLoader
from framework._utils.misc import datapath


class Identifier(str):
    ''' handling an identifier in source code. '''

    english_dictionary = enchant.Dict('en_US')
    re_word_spec = re.compile(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|[0-9]|$)')

    @classmethod
    def _readable(cls, word):
        ''' test if a word is readable in English. '''
        return len(word) > 1 and cls.english_dictionary.check(word)

    def _split_words(self):
        ''' returns splited identifier into words. '''
        return self.re_word_spec.findall(self)

    def readable(self):
        ''' test if all words in identifier is readable. '''
        return all(self._readable(word) for word in self._split_words())


class SourceProcessor(object):
    ''' handling processing over source code. '''

    def __init__(self, name, quoting=None, line_comment=None,
                 block_comment=None, keywords=None,
                 noise=r'[^a-zA-Z_0-9]', numeric=r'\b[0-9]+[ejl]?\b',
                 std_functions=None, lib_functions=None, **_):
        ''' make processor object with supplied langauge spec. '''
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
        ''' returns list of libraries defined in source. '''
        raise NotImplementedError

    def strip_string(self, sourcecode):
        ''' returns source without quoted string. '''
        return self.re_quoting.sub(' ', sourcecode)

    def strip_comment(self, sourcecode):
        ''' returns source without comment, must run after strip_string. '''
        if self.re_block_comment is not None:
            sourcecode = self.re_block_comment.sub(' ', sourcecode)
        return self.re_line_comment.sub(' ', sourcecode)

    def strip_keywords(self, sourcecode):
        ''' returns souce without keywords. '''
        return self.re_keywords.sub(' ', sourcecode)

    def strip_noise(self, sourcecode):
        ''' returns source without noise (operator, whitespace). '''
        return self.re_noise.sub(' ', sourcecode)

    def strip_numeric(self, sourcecode):
        ''' returns source without numeric representation. '''
        return self.re_numeric.sub(' ', sourcecode)

    def get_identifiers(self, sourcecode):
        ''' returns all identifiers with number of occurrences in source. '''
        intercode = self.strip_string(sourcecode)
        intercode = self.strip_comment(intercode)
        intercode = self.strip_keywords(intercode)
        intercode = self.strip_noise(intercode)
        intercode = self.strip_numeric(intercode)
        return Counter(intercode.split())

    def get_line_of_blocks(self, sourcecode):
        ''' returns number of lines of all blocks. '''
        if self.name == 'Python':
            return self._python_line_of_blocks(sourcecode)
        elif self.name in ['Java', 'C#']:
            return self._java_line_of_blocks(sourcecode)
        else:
            return self._cpp_line_of_blocks(sourcecode)

    def _python_line_of_blocks(self, sourcecode):
        ''' python-like spec for line of blocks. '''
        sourcecode = self.strip_comment(sourcecode)
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
        ''' cpp-like spec for line of blocks. '''
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
        ''' java-like spec for line of blocks. '''
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


class LazyLangDict(LazyLoader):
    ''' data of all language objects. '''
    @staticmethod
    def load_data():
        result = {}
        directory = datapath('_config', 'language')
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            language_spec = yaml.load(open(filepath))
            source_processor = SourceProcessor(**language_spec)
            for extension in language_spec['extensions']:
                result['.'+extension] = source_processor
        return result


def determine_languages(directory):
    ''' returns all known programming languages used in a directory. '''
    with LazyLangDict() as lang_dict:
        used_languages = set()
        for filename in os.listdir(directory):
            _, ext = os.path.splitext(filename)
            if ext in lang_dict:
                used_languages |= {lang_dict[ext].name}
        return used_languages


def select(ext):
    ''' main interface to use pre-defined language source processor. '''
    with LazyLangDict() as lang_dict:
        return lang_dict[ext.lower()]
