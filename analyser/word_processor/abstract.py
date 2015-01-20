import re
from collections import Counter


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

    def get_variable_names(self, sourcecode):
        intercode = self.strip_string(sourcecode)
        intercode = self.strip_comment(intercode)
        intercode = self.strip_keywords(intercode)
        intercode = self.strip_noise(intercode)
        return Counter(intercode.split())
