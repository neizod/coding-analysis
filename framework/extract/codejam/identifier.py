import os
import json

from ..._utils import datapath, iter_submission, readsource
from ..._utils import word_processor


def extract_identifier(year, force=False, quiet=False, **kwargs):
    os.makedirs(datapath('extract'), exist_ok=True)
    output_file = 'extract/identifier.json'
    if not force and os.path.isfile(datapath(output_file)):
        return
    extracted_data = []
    for pid, io, screen_name in iter_submission(year):
        directory = 'source/{}/{}/{}/'.format(pid, io, screen_name)
        quiet or log(directory)
        identifiers = set()
        for filename in os.listdir(datapath(directory)):
            if not os.path.isfile(datapath(directory, filename)):
                continue
            _, ext = os.path.splitext(datapath(directory, filename))
            try:
                prolang = word_processor.select(ext)
            except KeyError:
                continue
            sourcecode = readsource(datapath(directory, filename))
            identifiers |= prolang.get_variable_names(sourcecode).keys()
        quiet or log('  done\n')
        extracted_data += [{
            'pid': pid,
            'io': io,
            'screen_name': screen_name,
            'identifiers': sorted(identifiers),
        }]
    with open(datapath(output_file), 'w') as file:
        json.dump(extracted_data, file, indent=2)



def update_parser(subparsers):
    subparser = subparsers.add_parser('identifier', description='''
        This method will extract all identifiers in submitted source code
        from each contestants for futher analysis.''')
    subparser.add_argument('year', type=int, help='''
        year of a contest.''')
    subparser.add_argument('-f', '--force', action='store_true', help='''
        force extract even extracted data already exists.''')
    subparser.add_argument('-q', '--quiet', action='store_true', help='''
        run script quietly.''')
    subparser.set_defaults(function=extract_identifier)
