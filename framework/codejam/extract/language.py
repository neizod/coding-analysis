import os
import logging

from framework._utils import FunctionHook


class CodeJamExtractLanguage(FunctionHook):
    ''' This method will extract name of programming language used
        in each submission. '''

    def main(self, year, force=False, **_):
        from framework._utils import source, write
        from framework._utils.misc import datapath, make_ext
        from framework.codejam._helper import iter_submission
        os.makedirs(datapath('codejam', 'extract'), exist_ok=True)
        outpath = datapath('codejam', 'extract',
                           make_ext('language', year, 'json'))
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
                'languages': sorted(source.determine_languages(directory)),
            }]
        write.json(extracted_data, open(outpath, 'w'))
