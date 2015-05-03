import os
import json
import logging

from framework._utils import datapath, hook_common_arguments
from framework._utils import word_processor
from framework.codejam._helper import readsource, iter_submission


def main(year, force=False, **kwargs):
    os.makedirs(datapath('codejam', 'extract'), exist_ok=True)
    output_file = datapath('codejam', 'extract', 'identifier-{}.json'.format(year))
    if not force and os.path.isfile(output_file):
        return
    extracted_data = []
    for _, pid, io, screen_name in iter_submission(year):
        directory = datapath('codejam', 'source', pid, io, screen_name)
        logging.info('extracting: {} {} {}'.format(pid, io, screen_name))
        identifiers = set()
        for filename in os.listdir(directory):
            filepath = datapath('codejam', directory, filename)
            if not os.path.isfile(filepath):
                continue
            _, ext = os.path.splitext(filepath)
            try:
                prolang = word_processor.select(ext)
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
    with open(output_file, 'w') as file:
        json.dump(extracted_data, file, indent=2)


def update_parser(subparsers):
    subparser = subparsers.add_parser('identifier', description='''
        This method will extract all identifiers in submitted source code
        from each contestants for futher analysis.''')
    hook_common_arguments(subparser, main)
