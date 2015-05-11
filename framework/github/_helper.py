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


def iter_repos(language=None):
    ''' yields all repositories filtered by a programming language. '''
    with LazyMetadata() as metadata:
        for repo_language, repositories in metadata.items():
            if language is not None and repo_language != language:
                continue
            yield from repositories
