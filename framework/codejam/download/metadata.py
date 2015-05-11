import os
import logging

from framework._utils import FunctionHook


class CodeJamDownloadMetadata(FunctionHook):
    ''' This script will download Google Code Jam each round metadata
        of a suppliment year, and store each as JSON file. '''

    def main(self, year, force=False, **_):
        import json
        import urllib3
        from itertools import count
        from framework._utils import write
        from framework._utils.misc import datapath, make_ext
        from framework.codejam._helper import API, iter_contest
        http = urllib3.PoolManager()
        default = {'cmd': 'GetScoreboard', 'show_type': 'all'}
        os.makedirs(datapath('codejam', 'metadata', 'round'), exist_ok=True)
        for cid in iter_contest(year):
            filepath = datapath('codejam', 'metadata', 'round',
                                make_ext(cid, 'json'))
            if not force and os.path.isfile(filepath):
                logging.info('ignore: %i', cid)
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
            write.json(contest_stat, open(filepath, 'w'))
