import os
import json
import logging
from collections import defaultdict

from ..._utils import datapath, readsource, iter_submission


def find_plagiarism(contents):
    def compressed(submit):
        fields = ['io', 'screen_name']
        return {key: value for key, value in submit.items() if key in fields}
    plag_set = defaultdict(list)
    for submits in contents.values():
        if len({submit['screen_name'] for submit in submits}) > 1:
            pid = next(submit['pid'] for submit in submits)
            plag_set[pid] += [[compressed(submit) for submit in submits]]
    return [{'pid': pid, 'cheats': cheats} for pid, cheats in plag_set.items()]


def extract_cheat(year, force=False, **kwargs):
    os.makedirs(datapath('codejam', 'extract'), exist_ok=True)
    output_file = datapath('codejam', 'extract', 'cheat.json')
    if not force and os.path.isfile(output_file):
        return
    contents = defaultdict(list)
    for pid, io, screen_name in iter_submission(year):
        directory = datapath('codejam', 'source', pid, io, screen_name)
        logging.info('extracting: {} {} {}'.format(pid, io, screen_name))
        for filename in os.listdir(directory):
            filepath = datapath('codejam', directory, filename)
            if not os.path.isfile(filepath):
                continue
            sourcecode = readsource(filepath)
            if not sourcecode:
                continue
            contents[sourcecode] += [{'pid': pid, 'io': io, 'screen_name': screen_name}]
    extracted_data = find_plagiarism(contents)
    with open(output_file, 'w') as file:
        json.dump(extracted_data, file, indent=2)


def update_parser(subparsers):
    subparser = subparsers.add_parser('cheat', description='''
        This method will extract set of duplicated source codes.''')
    # TODO force
    subparser.add_argument('-f', '--force', action='store_true', help='''
        force''')
    subparser.add_argument('-q', '--quiet', action='store_const',
        const=logging.WARNING, help='''run the script quietly.''')
    subparser.set_defaults(function=extract_cheat)
