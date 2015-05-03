import os
import logging
import importlib


def submodules(_file, _name):
    return [importlib.import_module('.' + os.path.splitext(name)[0], _name)
            for name in os.listdir(os.path.dirname(_file))
            if not name.startswith(('.', '_'))]


def hook_submodules(parser, _file, _name):
    subparsers = parser.add_subparsers()
    for module in submodules(_file, _name):
        module.update_parser(subparsers)


def hook_common_arguments(parser):
    parser.add_argument('-f', '--force', action='store_true',
        help='''force run this method despite the exists result.''')
    parser.add_argument('-q', '--quiet', action='store_const',
        const=logging.WARNING, default=logging.INFO,
        help='''run this method without showing any information.''')


def make_ext(name, ext):
    return '{}{}{}'.format(name, os.extsep, ext)


def datapath(*ps):
    basepath = os.path.dirname(__file__)
    return os.path.join(basepath, '..', '..', 'data', *(str(p) for p in ps))
