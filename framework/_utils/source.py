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
    word_spec = re.compile(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|[0-9]|$)')

    @classmethod
    def _readable(cls, word):
        ''' test if a word is readable in English. '''
        return len(word) > 1 and cls.english_dictionary.check(word)

    def _split_words(self):
        ''' returns splited identifier into words. '''
        return re.findall(self.word_spec, self)

    def readable(self):
        ''' test if all words in identifier is readable. '''
        return all(self._readable(word) for word in self._split_words())


class SourceCode(object):
    ''' handling source code. '''

    @classmethod
    def determine_language(cls, filepath):
        ''' returns language used by looking at file name. '''
        with LazyLangDict() as lang_dict:
            ext = os.path.splitext(filepath)[-1]
            for _ in range(2):
                for lang_obj in lang_dict.values():
                    if ext in lang_obj['extensions']:
                        return lang_obj['name']
                ext = ext.lower()
            return NotImplemented

    @classmethod
    def open(cls, filepath, language=None):
        ''' make source code object by open file and guess used language. '''
        if language is None:
            language = cls.determine_language(filepath)
        try:
            code = open(filepath).read()
        except UnicodeError:
            code = open(filepath, encoding='latin1').read()
        return cls(code, language)

    def identifiers(self):
        ''' returns all identifiers with number of occurrences in source. '''
        return CodeSnippet(self.code, self.driver).identifiers()

    def __init__(self, code, language):
        ''' make source code object from providing code and language. '''
        self.code = code
        self.language = language
        self._init_driver()

    def _init_driver(self):
        ''' returns language driver for source code processing. '''
        with LazyLangDict() as lang_dict:
            try:
                self.driver = lang_dict[self.language]
            except KeyError:
                self.driver = NotImplemented


class CodeSnippet(object):
    ''' handling code snippet in source code. '''

    def identifiers(self):
        ''' returns all identifiers with number of occurrences in source. '''
        if self.driver is NotImplemented:
            raise NotImplementedError
        self._strip_string()
        self._strip_comment()
        self._strip_keywords()
        self._strip_noise()
        self._strip_numeric()
        return Counter(self.code.split())

    def extract_libraries(self, sourcecode):
        ''' returns list of libraries defined in source. '''
        raise NotImplementedError

    def __init__(self, code, driver):
        ''' make code snippet object with language driver. '''
        self.code = code
        self.driver = driver

    def _strip_string(self):
        ''' returns source without quoted string. '''
        pattern = self.driver['quoting']
        self.code = re.sub(pattern, ' ', self.code, flags=re.DOTALL)

    def _strip_comment(self):
        ''' returns source without comment, must run after strip_string. '''
        pattern = r'{}|{}(?=\n|$)'.format(self.driver['block_comment'],
                                          self.driver['line_comment'])
        self.code = re.sub(pattern, ' ', self.code, flags=re.DOTALL)

    def _strip_keywords(self):
        ''' returns souce without keywords. '''
        pattern = r'\b({})\b'.format('|'.join(self.driver['keywords']))
        self.code = re.sub(pattern, ' ', self.code)

    def _strip_noise(self):
        ''' returns source without noise (operator, whitespace). '''
        self.code = re.sub(self.driver['noise'], ' ', self.code)

    def _strip_numeric(self):
        ''' returns source without numeric representation. '''
        self.code = re.sub(self.driver['numeric'], ' ', self.code)


class LazyLangDict(LazyLoader):
    ''' data of all language objects. '''
    @staticmethod
    def load_data():
        directory = datapath('_config', 'language')
        defaults = yaml.load(open(datapath(directory, '_default.yaml')))
        filled = lambda spec: dict(defaults, **spec)
        specs = [filled(yaml.load(open(os.path.join(directory, filename))))
                 for filename in os.listdir(directory)
                 if filename != '_default.yaml']
        return {spec['name']: spec for spec in specs}
