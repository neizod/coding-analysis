import os
import sys
import inspect
import logging
import importlib
import argparse
import argcomplete


class LazyLoader(object):
    ''' handling data to be loaded on demand. '''

    data = NotImplemented

    @staticmethod
    def load_data():
        ''' override this method to tell what data looks like. '''
        raise NotImplementedError

    @classmethod
    def clear_data(cls):
        ''' call this method if loaded data need to be clear out. '''
        cls.data = NotImplemented

    def __enter__(self):
        ''' pre-load data if not exists. no need to modify this method. '''
        if self.data is NotImplemented:
            type(self).data = self.load_data()
        return self.data

    def __exit__(self, *_):
        ''' do nothing on exit. '''
        pass


class BaseParserHook(object):
    ''' handling argparse's subparser that defined over modules. '''

    def modify_parser(self):
        ''' override this method to modify parser after created. '''
        pass

    @classmethod
    def inject(cls, module):
        ''' inject module __file__/__name__ when try to create object. '''
        return lambda parser: cls(parser, module)

    def __init__(self, parser=None, module=None):
        ''' make parser/subparser and try to hook submodules. '''
        self._init_retrive_file_name(module)
        self._init_simple_parser(parser)
        self.modify_parser()
        self._init_hook_arguments()
        self._init_argcomplete(parser)

    def _init_retrive_file_name(self, defined_module):
        ''' init some values to help find location of submodules. '''
        if defined_module is None:
            defined_module = inspect.getmodule(type(self))
        self._file = defined_module.__file__
        self._name = defined_module.__name__

    def _init_simple_parser(self, parser):
        ''' init the parser. '''
        if parser is not None:
            parser_name = self._name.split('.')[-1].replace('_', '-')
            self.parser = parser.add_parser(parser_name)
        else:
            self.parser = argparse.ArgumentParser()
        self.parser.description = self.__doc__

    def _init_hook_arguments(self):
        ''' override this method to tell how to hook submodules/arguments. '''
        raise NotImplementedError

    def _init_argcomplete(self, parser):
        ''' init argcomplete to let using command line easier. '''
        if parser is None:
            argcomplete.autocomplete(self.parser)


class SubmodulesHook(BaseParserHook):
    ''' handling non-terminal perser to auto hook submodules. '''

    def _init_hook_arguments(self):
        subparsers = self.parser.add_subparsers()
        for cls in self._get_classes_from_submodules():
            if cls not in self._get_lineage_classes(sys.modules[__name__]):
                cls(subparsers)

    def _list_submodules(self):
        ''' yields all submodules that this module can reach. '''
        module_relpath = lambda name: '.{}'.format(os.path.splitext(name)[0])
        for name in os.listdir(os.path.dirname(self._file)):
            if not name.startswith(('.', '_')):
                yield importlib.import_module(module_relpath(name), self._name)

    def _get_classes_from_submodules(self):
        ''' yields all classes in submodules that this module can reach. '''
        for module in self._list_submodules():
            classes = list(self._get_lineage_classes(module))
            if classes:
                yield from iter(classes)
            elif os.path.split(module.__file__)[-1] == '__init__.py':
                yield self._dynamic_fake_subclass(module)

    @staticmethod
    def _get_lineage_classes(module):
        ''' yields all lineage of BaseParserHook defined in a module. '''
        for _, cls in inspect.getmembers(module):
            if inspect.isclass(cls) and issubclass(cls, BaseParserHook):
                yield cls

    @staticmethod
    def _dynamic_fake_subclass(module):
        ''' returns a new subclass of SubmodulesHook with fake name/file. '''
        return SubmodulesHook.inject(module)


class FunctionHook(BaseParserHook):
    ''' handling terminal perser to auto hook common arguments. '''

    def main(self):
        ''' override this method to tell what to do if this gets called. '''
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
    ''' handling terminal parser that doing analyse data. '''

    @staticmethod
    def analyse(data):
        ''' override this method to tell how to analyse data. '''
        raise NotImplementedError
