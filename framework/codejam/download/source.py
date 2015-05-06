import os
import urllib3
import logging

from framework._utils import FunctionHook, datapath
from framework.codejam._helper import API, iter_submission


class CodeJamDownloadMetadata(FunctionHook):
    def main(self, year, force=False, **_):
        http = urllib3.PoolManager()
        default = {'cmd': 'GetSourceCode'}
        for cid, pid, io, screen_name in iter_submission(year):
            directory = datapath('codejam', 'sourcezip', pid, io)
            os.makedirs(directory, exist_ok=True)
            zippath = datapath(directory, screen_name+'.zip')
            if not force and os.path.isfile(zippath):
                logging.info('ignore: %i %i %s', pid, io, screen_name)
                continue
            default['contest'] = cid
            default['problem'] = pid
            default['io_set_id'] = io
            default['username'] = screen_name
            logging.info('downloading: %i %i %s', pid, io, screen_name)
            result = http.request('GET', API, fields=default)
            with open(zippath, 'wb') as file:
                file.write(result.data)

    def modify_parser(self):
        self.parser.description = '''
            This script will download Google Code Jam submitted zipped sources.
            You need to run get_metadata script with supply argument of that year
            to build up list of contestants first.'''
