import os
import json
from collections import defaultdict

from ..._utils import datapath, readsource, log, iter_submission


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


def extract_cheat(year, force=False, quiet=False, **kwargs):
    os.makedirs(datapath('extract'), exist_ok=True)
    output_file = 'extract/cheat.json'
    if not force and os.path.isfile(datapath(output_file)):
        return
    contents = defaultdict(list)
    for pid, io, screen_name in iter_submission(year):
        directory = 'source/{}/{}/{}/'.format(pid, io, screen_name)
        quiet or log(directory)
        for filename in os.listdir(datapath(directory)):
            if not os.path.isfile(datapath(directory, filename)):
                continue
            sourcecode = readsource(datapath(directory, filename))
            contents[sourcecode] += [{'pid': pid, 'io': io, 'screen_name': screen_name}]
        quiet or log('  done\n')
    extracted_data = find_plagiarism(contents)
    with open(datapath(output_file), 'w') as file:
        json.dump(extracted_data, file, indent=2)


def update_parser(subparsers):
    subparser = subparsers.add_parser('cheat', description='''
        This method will extract set of duplicated source codes.''')
    # TODO force
    subparser.add_argument('-f', '--force', action='store_true', help='''
        force''')
    subparser.add_argument('-q', '--quiet', action='store_true', help='''
        run the script quietly.''')
    subparser.set_defaults(function=extract_cheat)
