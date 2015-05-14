import os
import json
import logging

from framework._utils import FunctionHook


class CodeJamExtractCyclomaticComplexity(FunctionHook):
    ''' This method will extract cyclomatic complexity from submitted code.
        Need to run `extract language` first, since not every language has
        implement with the extractor (only C, C++, Python). '''

    @staticmethod
    def use_cmetrics(pid, pio, uname):
        ''' cmetrics is a tool for analysing cyclomatic complexity for
            code written in C, C++. '''
        from subprocess import getoutput
        from framework._utils.misc import datapath
        directory = datapath('codejam', 'source', pid, pio, uname)
        data = getoutput('mccabe -n {}/*'.format(directory))
        if not data:
            return
        for line in data.split('\n'):
            *_, complexity, _ = line.split('\t')
            yield int(complexity)

    @staticmethod
    def use_radon(pid, pio, uname):
        ''' radon is a tool for analysing cyclomatic complexity for
            code written in Python. '''
        from subprocess import getoutput
        from framework._utils.misc import datapath
        directory = datapath('codejam', 'source', pid, pio, uname)
        data = json.loads(getoutput('radon cc -sj {}'.format(directory)))
        for extracted_file in data.values():
            if 'error' in extracted_file:
                return
            for extracted_func in extracted_file:
                yield extracted_func['complexity']

    def main(self, year, force=False, **_):
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        os.makedirs(datapath('codejam', 'extract'), exist_ok=True)
        usepath = datapath('codejam', 'extract',
                           make_ext('language', year, 'json'))
        outpath = datapath('codejam', 'extract',
                           make_ext('cyclomatic-complexity', year, 'json'))
        if not force and os.path.isfile(outpath):
            return logging.warn('output file already exists, aborting.')
        extracted_data = json.load(open(usepath))
        for submission in extracted_data:
            pid = submission['pid']
            pio = submission['io']
            uname = submission['uname']
            logging.info('extracting: %i %i %s', pid, pio, uname)
            languages_set = set(submission.pop('languages'))
            complexity = []
            if {'Python'} & languages_set:
                complexity += self.use_radon(pid, pio, uname)
            if {'C', 'C++'} & languages_set:
                complexity += self.use_cmetrics(pid, pio, uname)
            submission['cyclomatic-complexity'] = sorted(complexity)
        write.json(extracted_data, open(outpath, 'w'))
