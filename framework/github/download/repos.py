import os
import git
import logging

from framework._utils import SubparsersHook, datapath
from framework.github._helper import make_url, iter_repos


class GitHubDownloadRepos(SubparsersHook):
    def main(self, **_):
        os.makedirs(datapath('github', 'repos'), exist_ok=True)
        for repo in iter_repos():
            directory = datapath('github', 'repos', repo['name'])
            if not os.path.isdir(directory):
                logging.info('downloading: %s', repo['name'])
                git.Repo.clone_from(make_url(repo), directory)
            else:
                logging.info('updating: %s', repo['name'])
                git.Repo(directory).remotes.origin.pull()

    def modify_parser(self):
        self.parser.description = '''
            download/update git repositories from GitHub.'''
