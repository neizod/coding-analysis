import os
import logging

from framework._utils import FunctionHook


class CodeJamExtractIdentifier(FunctionHook):
    def main(self, year, force=False, **_):
        from framework._utils import datapath, source, write
        from framework.codejam._helper import readsource, iter_submission
        os.makedirs(datapath('codejam', 'extract'), exist_ok=True)
        output_file = datapath('codejam', 'extract', 'identifier-{}.json'.format(year))
        if not force and os.path.isfile(output_file):
            return logging.warn('output file already exists, aborting.')
        extracted_data = []
        for _, pid, io, screen_name in iter_submission(year):
            directory = datapath('codejam', 'source', pid, io, screen_name)
            logging.info('extracting: %i %i %s', pid, io, screen_name)
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
                identifiers |= prolang.get_variable_names(sourcecode).keys()
            extracted_data += [{
                'pid': pid,
                'io': io,
                'screen_name': screen_name,
                'identifiers': sorted(identifiers),
            }]
        write.json(extracted_data, open(output_file, 'w'))

    def modify_parser(self):
        self.parser.description = '''
            This method will extract all identifiers in submitted source code
            from each contestants for futher analysis.'''
