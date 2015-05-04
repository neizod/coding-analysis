import yaml

from framework._utils import datapath


api = 'https://github.com'
metadata = yaml.load(open(datapath('github', 'metadata.yaml')))


def make_url(repo):
    return '{}/{}/{}.git'.format(api, repo['user'], repo['name'])


def iter_repos(language=None):
    for repo_language, repos in metadata.items():
        if language is not None and repo_language != language:
            continue
        yield from repos
