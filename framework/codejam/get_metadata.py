#!/usr/bin/env python3

import json
import urllib3
import argparse
from itertools import count

import dry


def get_metadata(year, force=False, quiet=False):
    http = urllib3.PoolManager()
    api = dry.metadata['api']
    default = {'cmd': 'GetScoreboard', 'show_type': 'all'}
    dry.makedirs('metadata/round')
    for contest in dry.metadata[year]:
        filename = 'metadata/round/{}.json'.format(contest['id'])
        if not force and dry.isfile(filename):
            continue
        quiet or dry.log(contest['id'])
        default['contest_id'] = contest['id']
        contest_stat = []
        for i in count(1, 30):
            default['start_pos'] = i
            result = http.request('GET', api, fields=default)
            data = json.loads(result.data.decode('utf-8'))
            contest_stat += data['rows']
            quiet or dry.log('.')
            if i + 30 > data['stat']['nrp']:
                break
        with dry.open(filename, 'w') as file:
            json.dump(contest_stat, file, sort_keys=True, indent=4)
        quiet or dry.log('\n')


def main():
    parser = argparse.ArgumentParser(description='''
        This script will download Google Code Jam each round metadata
        of a suppliment year, and store each as JSON file.''')
    parser.add_argument('year', type=int, help='''
        year of a contest to download sources.''')
    parser.add_argument('-f', '--force', action='store_true', help='''
        force download metadata file if exists.''')
    parser.add_argument('-q', '--quiet', action='store_true', help='''
        run the script quietly.''')
    get_metadata(**vars(parser.parse_args()))


if __name__ == '__main__':
    main()
