import os
import logging

from framework._utils import FunctionHook


class GitHubDownloadRepos(FunctionHook):
    ''' download/update git repositories from GitHub.'''

    def main(self, **_):
        import git
        from framework._utils.misc import datapath
        from framework.github._helper import make_url, iter_repos
        os.makedirs(datapath('github', 'repos'), exist_ok=True)
        for repo in iter_repos():
            directory = datapath('github', 'repos', repo['name'])
            if not os.path.isdir(directory):
                logging.info('downloading: %s', repo['name'])
                git.Repo.clone_from(make_url(repo), directory)
            else:
                logging.info('updating: %s', repo['name'])
                git.Repo(directory).remotes.origin.pull()
