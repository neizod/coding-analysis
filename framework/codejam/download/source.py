import os
import logging

from framework._utils import FunctionHook


class CodeJamDownloadMetadata(FunctionHook):
    def main(self, year, force=False, **_):
        import urllib3
        from framework._utils import datapath, make_ext
        from framework.codejam._helper import API, iter_submission
        http = urllib3.PoolManager()
        default = {'cmd': 'GetSourceCode'}
        for cid, pid, pio, uname in iter_submission(year):
            directory = datapath('codejam', 'sourcezip', pid, pio)
            os.makedirs(directory, exist_ok=True)
            zippath = datapath(directory, make_ext(uname, 'zip'))
            if not force and os.path.isfile(zippath):
                logging.info('ignore: %i %i %s', pid, pio, uname)
                continue
            default['contest'] = cid
            default['problem'] = pid
            default['io_set_id'] = pio
            default['username'] = uname
            logging.info('downloading: %i %i %s', pid, pio, uname)
            result = http.request('GET', API, fields=default)
            open(zippath, 'wb').write(result.data)

    def modify_parser(self):
        self.parser.description = '''
            This script will download Google Code Jam submitted zipped sources.
            You need to run get_metadata script with supply argument of that
            year to build up list of contestants first.'''
