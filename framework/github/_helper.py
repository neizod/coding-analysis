import yaml

from framework._utils import datapath


API = 'https://github.com'
METADATA = yaml.load(open(datapath('github', 'metadata.yaml')))


def make_url(repo):
    return '{}/{}/{}.git'.format(API, repo['user'], repo['name'])


def iter_repos(language=None):
    for repo_language, repos in METADATA.items():
        if language is not None and repo_language != language:
            continue
        yield from repos
