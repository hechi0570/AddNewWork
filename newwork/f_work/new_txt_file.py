from copy import deepcopy
import json

metadata = {'metadata': {'kernelspec': {'display_name': 'Python 3',
                                        'language': 'python',
                                        'name': 'python3'},
                         'language_info': {'codemirror_mode': {'name': 'ipython', 'version': 3},
                                           'file_extension': '.py',
                                           'mimetype': 'text/x-python',
                                           'name': 'python',
                                           'nbconvert_exporter': 'python',
                                           'pygments_lexer': 'ipython3',
                                           'version': '3.9.5'}},
            'nbformat': 4,
            'nbformat_minor': 5}


class NewIpynb:
    '''创建一个默认格式的ipynb文件'''
    def __init__(self, file_path: str = '', file_name: str = ''):
        self._file_name = file_name
        self._file_path = file_path
        self.content = {'cells': []}
        self.cells = {'cell_type': 'code',
                        'execution_count': None,
                        'metadata': {},
                        'outputs': [],
                        'source': []}
    def create(self):
        '''写入默认数据'''
        content = deepcopy(self.content)
        cells: dict = deepcopy(self.cells)
        cells['source'].extend(
            ['import os\n', 'os.chdir(\'{}/{}\')'.format(self._file_path, self._file_name)])

        content['cells'].append(cells)
        c2 = deepcopy(self.cells)
        c2['source'].extend(['import pandas as pd\n', 'import numpy as np'])
        content['cells'].append(c2)
        content.update(metadata)
        # print(content)
        return json.dumps(content)