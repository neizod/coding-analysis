import os
import logging

from framework._utils import FunctionHook


class CodeJamExtractIdentifier(FunctionHook):
    ''' This method will extract all identifiers in submitted source code
        from each contestants for futher analysis. '''

    def main(self, year, force=False, **_):
        from framework._utils import source, write
        from framework._utils.misc import datapath, make_ext
        from framework.codejam._helper import readsource, iter_submission
        os.makedirs(datapath('codejam', 'extract'), exist_ok=True)
        outpath = datapath('codejam', 'extract',
                           make_ext('identifier', year, 'json'))
        if not force and os.path.isfile(outpath):
            return logging.warn('output file already exists, aborting.')
        extracted_data = []
        for _, pid, pio, uname in iter_submission(year):
            directory = datapath('codejam', 'source', pid, pio, uname)
            logging.info('extracting: %i %i %s', pid, pio, uname)
            identifiers = set()
            for filename in os.listdir(directory):
                filepath = datapath('codejam', directory, filename)
                if not os.path.isfile(filepath):
                    continue
                _, ext = os.path.splitext(filepath)
                try:
                    prolang = source.select(ext)
                except KeyError:
                    continue
                sourcecode = readsource(filepath)
                identifiers |= prolang.get_identifiers(sourcecode).keys()
            extracted_data += [{
                'pid': pid,
                'io': pio,
                'uname': uname,
                'identifiers': sorted(identifiers),
            }]
        write.json(extracted_data, open(outpath, 'w'))
