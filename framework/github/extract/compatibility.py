import os
import json
import logging

from framework._utils import FunctionHook


class GitHubExtractCompatibility(FunctionHook):
    ''' test compatibility over language versions. '''

    @staticmethod
    def handle_python(directory):
        ''' returns number of Python files in a repository that is syntactic
            compatible in Python 2/3. this method use standard Python program
            with module compileall to check. '''
        from subprocess import getoutput
        finder = 'find {} -name "{}" | wc -l'
        return (int(getoutput(('python2 -m compileall {} 2> /dev/null | '
                               'grep "File" | wc -l').format(directory))),
                int(getoutput(('python3 -m compileall {} 2> /dev/null | '
                               'grep "File" | wc -l').format(directory))),
                int(getoutput(finder.format(directory, '*.py'))))

    @staticmethod
    def handle_php(directory):
        ''' returns number of PHP files in a repository that is syntactic
            compatible in PHP 5.3~5.6. this method use standard PHP program
            (`php -l`), selection between PHP versions is done by phpbrew. '''
        from subprocess import getoutput
        check_php = (r'for file in $(find {} -name "*.php");'
                     r'do php -l "$file" &> /dev/null;'
                     r'[ $? != 0 ] && echo; done | wc -l').format(directory)
        args = '/bin/bash -c', '. ~/.phpbrew/bashrc', 'phpbrew use', check_php
        finder = 'find {} -name "{}" | wc -l'
        return (int(getoutput('{} \'{}; {} 5.3.29; {}\''.format(*args))),
                int(getoutput('{} \'{}; {} 5.4.38; {}\''.format(*args))),
                int(getoutput('{} \'{}; {} 5.5.22; {}\''.format(*args))),
                int(getoutput('{} \'{}; {} 5.6.6; {}\''.format(*args))),
                int(getoutput(finder.format(directory, '*.php'))))

    @staticmethod
    def git_snapshot(repo_obj, commit):
        ''' checkout repository snapshot at specific commit. '''
        if repo_obj.is_dirty():
            repo_obj.git.clean('-f')
            repo_obj.git.checkout('--')
        repo_obj.git.checkout(commit, '-f')
        return repo_obj

    def check_compat(self, lang, directory, done, limits=2):
        ''' returns syntactic compatibility of each repository over versions
            of the language over commit history. '''
        import git
        import random
        repo_obj = git.Repo(directory)
        latest_commit = repo_obj.head.reference
        do_only = [commit for commit in repo_obj.iter_commits()
                   if commit.hexsha not in {row['hash'] for row in done}]
        random.shuffle(do_only)
        for commit in do_only[:limits]:
            repo_obj = self.git_snapshot(repo_obj, commit)
            if lang == 'Python':
                py2, py3, files = self.handle_python(directory)
                yield {'date': commit.committed_date, 'hash': commit.hexsha,
                       'py2': py2, 'py3': py3, 'files': files}
            if lang == 'PHP':
                php53, php54, php55, php56, files = self.handle_php(directory)
                yield {'date': commit.committed_date, 'hash': commit.hexsha,
                       'php53': php53, 'php54': php54, 'php55': php55,
                       'php56': php56, 'files': files}
        repo_obj = self.git_snapshot(repo_obj, latest_commit)

    def main(self, only_repo=None, only_lang=None, count=1, **_):
        from framework._utils import write
        from framework._utils.misc import datapath
        from framework.github._helper import iter_repos
        os.makedirs(datapath('github', 'extract'), exist_ok=True)
        filepath = datapath('github', 'extract', 'compatibility.json')
        if os.path.isfile(filepath):
            extracted_data = json.load(open(filepath))
        else:
            extracted_data = {}
        for lang, repo in iter_repos():
            if only_lang is not None and lang.lower() != only_lang.lower():
                continue
            if only_repo is not None and repo['name'] != only_repo:
                continue
            directory = datapath('github', 'repos', repo['name'])
            logging.info('extract: %s', repo['name'])
            if repo['name'] not in extracted_data:
                extracted_data[repo['name']] = []
            done = extracted_data[repo['name']]
            done += self.check_compat(lang, directory, done, limits=count)
            done.sort(key=lambda row: row['date'])
        write.json(extracted_data, open(filepath, 'w'))

    def modify_parser(self):
        self.parser.add_argument(
            '-r', '--only-repo', help='''only this repository.''')
        self.parser.add_argument(
            '-l', '--only-lang', help='''only this language.''')
        self.parser.add_argument(
            '-c', '--count', type=int, default=1,
            help='''limit checkout count.''')
