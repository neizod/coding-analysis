import os
import inspect
import logging
import importlib
import argparse
import argcomplete


class SubparsersHook(object):
    def main(self):
        if os.path.split(self._file)[-1] != '__init__.py':
            raise NotImplementedError

    def modify_parser(self):
        pass

    def __init__(self, parser=None):
        self._name = inspect.getmodule(type(self)).__name__
        self._file = inspect.getfile(type(self))
        self._make_simple_parser(parser)
        self.modify_parser()
        if os.path.split(self._file)[-1] == '__init__.py':
            self._hook_submodules()
        else:
            self._hook_common_arguments()
        if len(self._name.split('.')) == 1:
            argcomplete.autocomplete(self.parser)

    def _make_simple_parser(self, parser):
        if parser is not None:
            parser_name = self._name.split('.')[-1].replace('_', '-')
            self.parser = parser.add_parser(parser_name)
        else:
            self.parser = argparse.ArgumentParser()

    def _list_submodules(self):
        module_relpath = lambda name: '.{}'.format(os.path.splitext(name)[0])
        for name in os.listdir(os.path.dirname(self._file)):
            if not name.startswith(('.', '_')):
                yield importlib.import_module(module_relpath(name), self._name)

    def _get_classes_from_submodules(self):
        for module in self._list_submodules():
            for _, cls in inspect.getmembers(module):
                if inspect.isclass(cls):
                    yield cls

    def _hook_submodules(self):
        subparsers = self.parser.add_subparsers()
        for cls in self._get_classes_from_submodules():
            if issubclass(cls, SubparsersHook) and cls != SubparsersHook:
                cls(subparsers)

    def _hook_common_arguments(self):
        self.parser.add_argument('-f', '--force', action='store_true',
            help='''force run this method despite the exists result.''')
        self.parser.add_argument('-q', '--quiet', action='store_const',
            const=logging.WARNING, default=logging.INFO,
            help='''run this method without showing any information.''')
        self.parser.set_defaults(function=self.main)


def make_ext(name, ext):
    return '{}{}{}'.format(name, os.extsep, ext)


def datapath(*ps):
    basepath = os.path.dirname(__file__)
    return os.path.join(basepath, '..', '..', 'data', *(str(p) for p in ps))
