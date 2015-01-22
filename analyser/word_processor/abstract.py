import re
import enchant
from collections import Counter


class Identifier(object):

    english_dictionary = enchant.Dict('en_US')
    word_spec = re.compile(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|[0-9]|$)')

    @classmethod
    def _readable(cls, word):
        return len(word) > 1 and cls.english_dictionary.check(word)

    @classmethod
    def is_readable(cls, identifier):
        return all(cls._readable(word) for word in cls.word_spec.findall(identifier))



class WordProcessor(object):

    def __init__(self, quoting=None,
                       comment=None,
                       keywords=None,
                       noise=None,
                       std_functions=None,
                       lib_functions=None ):
        self.quoting = quoting
        self.comment = comment
        self.keywords = keywords
        self.noise = noise
        self.std_functions = std_functions
        self.lib_functions = lib_functions

    def extract_libraries(self, sourcecode):
        pass

    def strip_string(self, sourcecode):
        return re.sub(self.quoting, ' ', sourcecode, flags=re.DOTALL)

    def strip_comment(self, sourcecode):
        if self.comment[0]:
            sourcecode = re.sub(self.comment[0], '', sourcecode, flags=re.DOTALL)
        return re.sub(self.comment[1], ' ', sourcecode)

    def strip_keywords(self, sourcecode):
        keywords_pattern = '|'.join(self.keywords)
        return re.sub(keywords_pattern, ' ', sourcecode)

    def strip_noise(self, sourcecode):
        return re.sub(self.noise, ' ', sourcecode)

    def strip_numeric(self, sourcecode):
        return re.sub(r'\b[0-9]+\b', ' ', sourcecode)

    def get_variable_names(self, sourcecode):
        intercode = self.strip_string(sourcecode)
        intercode = self.strip_comment(intercode)
        intercode = self.strip_keywords(intercode)
        intercode = self.strip_noise(intercode)
        intercode = self.strip_numeric(intercode)
        return Counter(intercode.split())
