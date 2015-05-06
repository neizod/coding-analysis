import os
import yaml

from framework._utils import datapath
from .abstract import WordProcessor, Identifier


_LANG_DICT = None

def select(ext):
    global _LANG_DICT
    if _LANG_DICT is None:
        _LANG_DICT = {}
        directory = datapath('_config', 'language')
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            language_spec = yaml.load(open(filepath))
            it = WordProcessor(**language_spec)
            for extension in language_spec['extensions']:
                _LANG_DICT['.'+extension] = it
    return _LANG_DICT[ext.lower()]
