import os
import inspect
import logging
import importlib
import argparse
import argcomplete


class SubparsersHook(object):

    _fake = None

    def main(self):
        if os.path.split(self._file)[-1] != '__init__.py':
            raise NotImplementedError

    def modify_parser(self):
        pass

    def __init__(self, parser=None):
        self._init_handle_name_file()
        self._init_simple_parser(parser)
        self.modify_parser()
        self._init_decide_hook_method()

    def _init_handle_name_file(self):
        if self._fake is not None:
            structure = self._fake.split('.') + ['__init__.py']
            directory, last = os.path.split(__file__)
            while last != structure[0]:
                directory, last = os.path.split(directory)
            self._file = os.path.join(directory, *structure)
            self._name = self._fake
        else:
            defined_module = inspect.getmodule(type(self))
            self._file = defined_module.__file__
            self._name = defined_module.__name__

    def _init_decide_hook_method(self):
        if os.path.split(self._file)[-1] == '__init__.py':
            self._hook_submodules()
        else:
            self._hook_common_arguments()
        if len(self._name.split('.')) == 1:
            argcomplete.autocomplete(self.parser)

    def _init_simple_parser(self, parser):
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
            if not hasattr(module, '__file__'):
                yield type('', (SubparsersHook,), {'_fake': module.__name__})
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
