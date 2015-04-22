import os
import json

from ... import utils
from ...utils import word_processor


def extract_identifier(year, force=False, quiet=False, **kwargs):
    os.makedirs(utils.data('extract'), exist_ok=True)
    output_file = 'extract/identifier.json'
    if not force and os.path.isfile(utils.data(output_file)):
        return
    extracted_data = []
    for pid, io, screen_name in utils.iter_submission(year):
        directory = 'source/{}/{}/{}/'.format(pid, io, screen_name)
        quiet or utils.log(directory)
        identifiers = set()
        for filename in os.listdir(utils.data(directory)):
            if not os.path.isfile(utils.data(directory, filename)):
                continue
            _, ext = os.path.splitext(utils.data(directory, filename))
            try:
                prolang = word_processor.select(ext)
            except KeyError:
                continue
            sourcecode = utils.readsource(utils.data(directory, filename))
            identifiers |= prolang.get_variable_names(sourcecode).keys()
        quiet or utils.log('  done\n')
        extracted_data += [{
            'pid': pid,
            'io': io,
            'screen_name': screen_name,
            'identifiers': sorted(identifiers),
        }]
    with open(utils.data(output_file), 'w') as file:
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
