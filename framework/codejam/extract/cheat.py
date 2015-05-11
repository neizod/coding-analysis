import os
import logging

from framework._utils import FunctionHook


class CodeJamExtractCheat(FunctionHook):
    ''' This method will extract set of duplicated source codes. '''

    @staticmethod
    def find_plagiarism(contents):
        ''' returns all set of names which has same source code. '''
        from collections import defaultdict
        compressed = lambda submit: {key: value
                                     for key, value in submit.items()
                                     if key in {'io', 'uname'}}
        plag = defaultdict(list)
        for submits in contents.values():
            if len({submit['uname'] for submit in submits}) > 1:
                pid = next(submit['pid'] for submit in submits)
                plag[pid] += [[compressed(submit) for submit in submits]]
        return [{'pid': pid, 'cheats': cheats} for pid, cheats in plag.items()]

    def main(self, year, force=False, **_):
        from collections import defaultdict
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        from framework.codejam._helper import readsource, iter_submission
        os.makedirs(datapath('codejam', 'extract'), exist_ok=True)
        outpath = datapath('codejam', 'extract',
                           make_ext('cheat', year, 'json'))
        if not force and os.path.isfile(outpath):
            return logging.warn('output file already exists, aborting.')
        contents = defaultdict(list)
        for _, pid, pio, uname in iter_submission(year):
            directory = datapath('codejam', 'source', pid, pio, uname)
            logging.info('extracting: %i %i %s', pid, pio, uname)
            for filename in os.listdir(directory):
                filepath = datapath('codejam', directory, filename)
                if not os.path.isfile(filepath):
                    continue
                code = readsource(filepath)
                if not code:
                    continue
                contents[code] += [{'pid': pid, 'io': pio, 'uname': uname}]
        extracted_data = self.find_plagiarism(contents)
        write.json(extracted_data, open(outpath, 'w'), depth=4)
