import os
import json

from ..._utils import datapath, log, iter_submission, readsource
from ..._utils import word_processor


def extract_identifier(year, force=False, quiet=False, **kwargs):
    os.makedirs(datapath('extract'), exist_ok=True)
    output_file = 'extract/language.json'
    if not force and os.path.isfile(datapath(output_file)):
        return
    extracted_data = []
    for pid, io, screen_name in iter_submission(year):
        directory = 'source/{}/{}/{}/'.format(pid, io, screen_name)
        quiet or log(directory)
        languages = set()
        for filename in os.listdir(datapath(directory)):
            if not os.path.isfile(datapath(directory, filename)):
                continue
            _, ext = os.path.splitext(datapath(directory, filename))
            try:
                prolang = word_processor.select(ext)
            except KeyError:
                continue
            languages |= {prolang.name}
        quiet or log('  done\n')
        extracted_data += [{
            'pid': pid,
            'io': io,
            'screen_name': screen_name,
            'language': languages.pop() if len(languages) == 1 else None,
        }]
    with open(datapath(output_file), 'w') as file:
        json.dump(extracted_data, file, indent=2)



def update_parser(subparsers):
    subparser = subparsers.add_parser('language', description='''
        This method will extract name of programming language used
        in each submission.''')
    subparser.add_argument('-f', '--force', action='store_true', help='''
        force override output.''')
    subparser.add_argument('-q', '--quiet', action='store_true', help='''
        run script quietly.''')
    subparser.set_defaults(function=extract_identifier)
