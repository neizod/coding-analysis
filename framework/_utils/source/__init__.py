import os
import yaml

from framework._utils import datapath
from .abstract import WordProcessor, Identifier


_LANG_DICT = {}


def _lazy_init():
    if not _LANG_DICT:
        directory = datapath('_config', 'language')
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            language_spec = yaml.load(open(filepath))
            source_processor = WordProcessor(**language_spec)
            for extension in language_spec['extensions']:
                _LANG_DICT['.'+extension] = source_processor


def determine_languages(directory):
    _lazy_init()
    used_languages = set()
    for filename in os.listdir(directory):
        _, ext = os.path.splitext(filename)
        if ext in _LANG_DICT:
            used_languages |= {_LANG_DICT[ext].name}
    return used_languages


def select(ext):
    _lazy_init()
    return _LANG_DICT[ext.lower()]
