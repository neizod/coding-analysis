import yaml

from framework._utils import LazyLoader, datapath


API = 'https://github.com'


class LazyMetadata(LazyLoader):
    @staticmethod
    def load_data():
        return yaml.load(open(datapath('github', 'metadata.yaml')))


def make_url(repo):
    return '{}/{}/{}.git'.format(API, repo['user'], repo['name'])


def iter_repos(language=None):
    with LazyMetadata() as metadata:
        for repo_language, repositories in metadata.items():
            if language is not None and repo_language != language:
                continue
            yield from repositories
