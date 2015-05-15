import os
import yaml

from framework._utils import LazyLoader
from framework._utils.misc import datapath, make_ext


API = 'https://github.com'


class LazyMetadata(LazyLoader):
    ''' metadata for GitHub repositories. '''
    @staticmethod
    def load_data():
        return yaml.load(open(datapath('github', 'metadata.yaml')))


def make_url(repo):
    ''' returns url to a github repository. '''
    return os.path.join(API, repo['user'], make_ext(repo['name'], 'git'))


def iter_repos():
    ''' yields all repositories along side with language using. '''
    with LazyMetadata() as metadata:
        for language, repositories in metadata.items():
            yield from ((language, repository) for repository in repositories)
