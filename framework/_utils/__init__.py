import os
import sys
import inspect
import logging
import importlib
import argparse
import argcomplete
from operator import add
from functools import reduce


class LazyLoader(object):

    data = NotImplemented

    @staticmethod
    def load_data():
        raise NotImplementedError

    def __enter__(self):
        if self.data is NotImplemented:
            type(self).data = self.load_data()
        return self.data

    def __exit__(self, *_):
        pass


class BaseParserHook(object):
    def modify_parser(self):
        pass

    def __init__(self, parser=None):
        self._init_handle_name_file()
        self._init_simple_parser(parser)
        self.modify_parser()
        self._init_hook_arguments()
        self._init_argcomplete(parser)

    def _init_handle_name_file(self):
        defined_module = inspect.getmodule(type(self))
        self._file = defined_module.__file__
        self._name = defined_module.__name__

    def _init_simple_parser(self, parser):
        if parser is not None:
            parser_name = self._name.split('.')[-1].replace('_', '-')
            self.parser = parser.add_parser(parser_name)
        else:
            self.parser = argparse.ArgumentParser()

    def _init_hook_arguments(self):
        raise NotImplementedError

    def _init_argcomplete(self, parser):
        if parser is None:
            argcomplete.autocomplete(self.parser)


class SubmodulesHook(BaseParserHook):
    def _init_hook_arguments(self):
        subparsers = self.parser.add_subparsers()
        for cls in self._get_classes_from_submodules():
            if cls not in self._get_lineage_classes(sys.modules[__name__]):
                cls(subparsers)

    def _list_submodules(self):
        module_relpath = lambda name: '.{}'.format(os.path.splitext(name)[0])
        for name in os.listdir(os.path.dirname(self._file)):
            if not name.startswith(('.', '_')):
                yield importlib.import_module(module_relpath(name), self._name)

    def _get_classes_from_submodules(self):
        for module in self._list_submodules():
            if not hasattr(module, '__file__'):
                yield self._dynamic_fake_subclass(module.__name__)
            yield from self._get_lineage_classes(module)

    @staticmethod
    def _get_lineage_classes(module):
        for _, cls in inspect.getmembers(module):
            if inspect.isclass(cls) and issubclass(cls, BaseParserHook):
                yield cls

    @staticmethod
    def _dynamic_fake_subclass(module_name):
        class FakeHook(SubmodulesHook):
            def _init_handle_name_file(self):
                structure = module_name.split('.') + ['__init__.py']
                directory, last = os.path.split(__file__)
                while last != structure[0]:
                    directory, last = os.path.split(directory)
                self._file = os.path.join(directory, *structure)
                self._name = module_name
        return FakeHook


class FunctionHook(BaseParserHook):
    def main(self):
        raise NotImplementedError

    def _init_hook_arguments(self):
        self.parser.add_argument(
            '-f', '--force', action='store_true',
            help='''force run this method despite the exists result.''')
        self.parser.add_argument(
            '-q', '--quiet', action='store_const',
            const=logging.WARNING, default=logging.INFO,
            help='''run this method without showing any information.''')
        self.parser.set_defaults(function=self.main)


class AnalyserHook(FunctionHook):
    def analyse(self):
        raise NotImplementedError


def make_ext(name, ext):
    return '{}{}{}'.format(name, os.extsep, ext)


def datapath(*ps):
    basepath = os.path.dirname(__file__)
    return os.path.join(basepath, '..', '..', 'data', *(str(p) for p in ps))


def flat_zip(*iterators):
    wrap = lambda obj: (obj,) if not isinstance(obj, tuple) else obj
    iterators = [iter(iterator) for iterator in iterators]
    while True:
        yield reduce(add, [wrap(next(iterator)) for iterator in iterators])
