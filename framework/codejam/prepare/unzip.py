import os
import logging

from framework._utils import FunctionHook


class CodeJamPrepareUnzip(FunctionHook):
    @staticmethod
    def ensure_recursive_unzip(year):
        from zipfile import ZipFile, BadZipFile
        for _, pid, io, screen_name in iter_submission(year):
            directory = datapath('codejam', 'source', pid, io, screen_name)
            for filename in os.listdir(directory):
                filepath = datapath('codejam', directory, filename)
                if os.path.splitext(filepath)[1] == '.zip':
                    with ZipFile(filepath) as z:
                        z.extractall(directory)
                    os.remove(filepath)

    def main(self, year, force=False, **_):
        from zipfile import ZipFile, BadZipFile
        from framework._utils import datapath
        from framework.codejam._helper import iter_submission
        bad_zipfiles = []
        for _, pid, io, screen_name in iter_submission(year):
            zippath = datapath('codejam', 'sourcezip', pid, io, screen_name+'.zip')
            directory = datapath('codejam', 'source', pid, io, screen_name)
            os.makedirs(directory, exist_ok=True)
            logging.info('unzipping: %i %i %s', pid, io, screen_name)
            if force or not os.listdir(directory):
                try:
                    with ZipFile(zippath) as z:
                        z.extractall(directory)
                except BadZipFile:
                    bad_zipfiles += [zippath]
        if bad_zipfiles:
            for zippath in bad_zipfiles:
                os.renames(zippath, datapath('codejam', 'badzip', zippath))
            raise BadZipFile(bad_zipfiles)
        self.ensure_recursive_unzip(year)

    def modify_parser(self):
        self.parser.description = '''
            This method will unzip downloaded source code files.'''
