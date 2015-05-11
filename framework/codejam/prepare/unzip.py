import os
import logging

from framework._utils import FunctionHook


class CodeJamPrepareUnzip(FunctionHook):
    ''' This method will unzip downloaded source code files. '''

    @staticmethod
    def ensure_recursive_unzip(year):
        ''' some of the contestants will zip their work before submit answer
            since they want to submit multiple files or size of submit files
            are larger than the accepted policy, so 2nd unzip is require. '''
        from zipfile import ZipFile
        from framework._utils.misc import datapath
        from framework.codejam._helper import iter_submission
        for _, pid, pio, uname in iter_submission(year):
            directory = datapath('codejam', 'source', pid, pio, uname)
            for filename in os.listdir(directory):
                filepath = datapath('codejam', directory, filename)
                if os.path.splitext(filepath)[1] == '.zip':
                    ZipFile(filepath).extractall(directory)
                    os.remove(filepath)

    def main(self, year, force=False, **_):
        from zipfile import ZipFile, BadZipFile
        from framework._utils.misc import datapath, make_ext
        from framework.codejam._helper import iter_submission
        bad_zipfiles = []
        for _, pid, pio, uname in iter_submission(year):
            zipname = make_ext(uname, 'zip')
            zippath = datapath('codejam', 'sourcezip', pid, pio, zipname)
            directory = datapath('codejam', 'source', pid, pio, uname)
            os.makedirs(directory, exist_ok=True)
            logging.info('unzipping: %i %i %s', pid, pio, uname)
            if force or not os.listdir(directory):
                try:
                    ZipFile(zippath).extractall(directory)
                except BadZipFile:
                    bad_zipfiles += [zippath]
        if bad_zipfiles:
            for zippath in bad_zipfiles:
                os.renames(zippath, datapath('codejam', 'badzip', zippath))
            raise BadZipFile(bad_zipfiles)
        self.ensure_recursive_unzip(year)
