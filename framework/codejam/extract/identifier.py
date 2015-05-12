import os
import logging

from framework._utils import FunctionHook


class CodeJamExtractIdentifier(FunctionHook):
    ''' This method will extract all identifiers in submitted source code
        from each contestants for futher analysis. '''

    @staticmethod
    def get_identifiers(directory):
        ''' returns all identifiers in source code files in a directory. '''
        from framework._utils.misc import datapath
        from framework._utils.source import SourceCode
        identifiers = set()
        for filename in os.listdir(directory):
            filepath = datapath('codejam', directory, filename)
            if not os.path.isfile(filepath):
                continue
            source_code = SourceCode.open(filepath)
            try:
                identifiers |= source_code.get_identifiers().keys()
            except NotImplementedError:
                continue
        return identifiers

    def main(self, year, force=False, **_):
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        from framework.codejam._helper import iter_submission
        os.makedirs(datapath('codejam', 'extract'), exist_ok=True)
        outpath = datapath('codejam', 'extract',
                           make_ext('identifier', year, 'json'))
        if not force and os.path.isfile(outpath):
            return logging.warn('output file already exists, aborting.')
        extracted_data = []
        for _, pid, pio, uname in iter_submission(year):
            directory = datapath('codejam', 'source', pid, pio, uname)
            logging.info('extracting: %i %i %s', pid, pio, uname)
            extracted_data += [{
                'pid': pid,
                'io': pio,
                'uname': uname,
                'identifiers': sorted(self.get_identifiers(directory)),
            }]
        write.json(extracted_data, open(outpath, 'w'))
