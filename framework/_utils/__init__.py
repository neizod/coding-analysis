import os
import importlib


def submodules(_file, _name):
    return [importlib.import_module('.' + os.path.splitext(name)[0], _name)
            for name in os.listdir(os.path.dirname(_file))
            if not name.startswith(('.', '_'))]


def hook_submodules(parser, _file, _name):
    subparsers = parser.add_subparsers()
    for module in submodules(_file, _name):
        module.update_parser(subparsers)


def make_ext(name, ext):
    return '{}{}{}'.format(name, os.extsep, ext)


def datapath(*ps):
    basepath = os.path.dirname(__file__)
    return os.path.join(basepath, '..', '..', 'data', *(str(p) for p in ps))
