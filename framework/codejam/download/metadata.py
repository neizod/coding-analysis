import os
import json
import urllib3
import logging
from itertools import count

from framework._utils import FunctionHook, datapath
from framework.codejam._helper import API, iter_contest


class CodeJamDownloadMetadata(FunctionHook):
    def main(self, year, force=False, **_):
        http = urllib3.PoolManager()
        default = {'cmd': 'GetScoreboard', 'show_type': 'all'}
        os.makedirs(datapath('codejam', 'metadata', 'round'), exist_ok=True)
        for cid in iter_contest(year):
            filepath = datapath('codejam', 'metadata', 'round', str(cid)+'.json')
            if not force and os.path.isfile(filepath):
                continue
            default['contest_id'] = cid
            contest_stat = []
            for i in count(1, 30):
                default['start_pos'] = i
                result = http.request('GET', API, fields=default)
                data = json.loads(result.data.decode('utf-8'))
                contest_stat += data['rows']
                logging.info('downloading: %i %i', cid, i)
                if i + 30 > data['stat']['nrp']:
                    break
            with open(filepath, 'w') as file:
                json.dump(contest_stat, file, sort_keys=True, indent=4)

    def modify_parser(self):
        self.parser.description = '''
            This script will download Google Code Jam each round metadata
            of a suppliment year, and store each as JSON file.'''
