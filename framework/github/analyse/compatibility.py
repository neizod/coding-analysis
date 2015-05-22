import os
import json

from framework._utils import AnalyserHook


class GitHubAnalyseCompatibility(AnalyserHook):
    ''' analyse compatibility over language versions. '''

    @staticmethod
    def analyse(data):
        import time
        from framework.github._helper import iter_repos
        ymd = lambda epoch: time.strftime('%Y-%m-%d', time.gmtime(epoch))
        results = {'Python': [], 'PHP': []}
        for language, repo in iter_repos():
            if repo['name'] not in data:
                continue
            for row in data[repo['name']]:
                sum_row = [repo['name'], ymd(row['date']), row['files']]
                if language == 'Python':
                    sum_row += [row['py2'], row['py3']]
                if language == 'PHP':
                    sum_row += [row['php53'], row['php54'],
                                row['php55'], row['php56']]
                results[language] += [sum_row]
        return results

    @staticmethod
    def prepare_input(**_):
        from framework._utils.misc import datapath
        os.makedirs(datapath('github', 'result'), exist_ok=True)
        usepath = datapath('github', 'extract', 'compatibility.json')
        return json.load(open(usepath))

    @staticmethod
    def prepare_output(results, **_):
        from itertools import chain
        from framework._utils import write
        from framework._utils.misc import datapath
        analyse_data = [
            (['repo', 'date', 'files', 'py2', 'py3'],
             datapath('github', 'result', 'compatibility-python.txt'),
             results['Python']),
            (['repo', 'date', 'files', 'php53', 'php54', 'php55', 'php56'],
             datapath('github', 'result', 'compatibility-php.txt'),
             results['PHP'])]
        for header, outpath, result in analyse_data:
            write.table(chain([header], result), open(outpath, 'w'))
