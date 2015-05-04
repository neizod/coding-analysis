import os
import git
import logging

from framework._utils import datapath, hook_common_arguments
from framework.github._helper import make_url, iter_repos


def main(**_):
    os.makedirs(datapath('github', 'repos'), exist_ok=True)
    for repo in iter_repos():
        directory = datapath('github', 'repos', repo['name'])
        if not os.path.isdir(directory):
            logging.info('downloading: {}'.format(repo['name']))
            git.Repo.clone_from(make_url(repo), directory)
        else:
            logging.info('updating: {}'.format(repo['name']))
            git.Repo(directory).remotes.origin.pull()


def update_parser(subparsers):
    subparser = subparsers.add_parser('repos', description='''
        download/update git repositories from GitHub.''')
    hook_common_arguments(subparser, main)
