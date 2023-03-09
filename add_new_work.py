import os
from datetime import datetime
from copy import deepcopy
import json
import shutil
import PySimpleGUI as sg


WorkPath = 'D:/Work'
IpynbPath = 'C:/he/notebook/Wrok'
# WxPath = r'D:\Program Files (x86)\Tencent\wechatfiles\WeChat Files\qepbagss\FileStorage\File\2022-09'
# IpynbPath = '.'

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


class NewWork:
    def __init__(self) -> None:
        self.today: str = datetime.today().strftime('%y%m%d')
        self.content = {'cells': []}
        self.cells = {'cell_type': 'code',
                      'execution_count': None,
                      'metadata': {},
                      'outputs': [],
                      'source': []}
        self.wx_path = r'D:\Program Files (x86)\Tencent\wechatfiles\WeChat Files\qepbagss\FileStorage\File\2022-09'
        self.work_path = 'D:/Work'

    def create_folder(self, date: str = None):
        '''建立工作目录'''
        if date is None:
            date = self.today
        try:
            os.mkdir(os.path.join(WorkPath, date))
        except FileExistsError:
            raise FileExistsError
        print('工作目录创建成功')

    def create_ipynb(self, date: str = None):
        '''建立 jupyter 文件'''
        if date is None:
            date = self.today
        self.filename = f'{date}.ipynb'
        file_path = os.path.join(IpynbPath, self.filename)

        if self.filename in os.listdir(IpynbPath):
            raise FileExistsError

        with open(file_path, 'w') as f:
            f.write(self.ipynb_write())
        print('ipynb 文件创建成功')

    def ipynb_write(self):
        content = deepcopy(self.content)
        cells: dict = deepcopy(self.cells)
        cells['source'].extend(
            ['import os\n', 'os.chdir(\'{}/{}\')'.format(WorkPath, self.today)])

        content['cells'].append(cells)
        c2 = deepcopy(self.cells)
        c2['source'].extend(['import pandas as pd\n', 'import numpy as np'])
        content['cells'].append(c2)
        content.update(metadata)
        # print(content)
        return json.dumps(content)

    def clear_item(self):
        '''清除创建的文件和文件夹'''
        # os.removedirs(os.path.join(WorkPath, self.today))
        shutil.rmtree(os.path.join(WorkPath, self.today))
        os.remove(os.path.join(IpynbPath, f'{self.today}.ipynb'))

    def show_item_files(self, path, itemname=None, only_path: bool = False):
        '''显示项目文件夹中的文件
        only_path: 直接传入路径, 不需要拼接
        '''
        def sort_fils(dic: dict) -> list:
            # 将 dict 排序后返回排序好的键
            dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)
            # print('RRR', dic)
            return list(dict(dic).keys())

        if only_path:
            item_path = path
        else:
            if itemname is None:
                itemname = self.today
            item_path = os.path.join(path, itemname)
        try:
            # file_ls = os.listdir(item_path)
            file_dic = {f: os.path.getmtime(os.path.join(
                item_path, f)) for f in os.listdir(item_path)}
            file_ls = sort_fils(file_dic)
        except FileNotFoundError:
            file_ls = ['未发现项目文件夹']
        return file_ls

    def copy_item_flies(self, files: list, itemname=None, is_gui: bool = None):
        '''将选定的文件复制到项目文件夹
        is_gui: 是否为gui程序调用, 如果是就返回弹窗
        '''
        if itemname is None:
            itemname = self.today
        for filename in files:
            if filename in os.listdir(os.path.join(WorkPath, itemname)):
                if is_gui:
                    msg = sg.popup_yes_no(f'{filename}已存在，是否覆盖!')
                else:
                    msg = 'Yes'
            else:
                msg = 'Yes'

            if msg != 'Yes':
                break
            
            src_file = os.path.join(self.wx_path, filename)
            if os.path.isfile(src_file):
                shutil.copy2(
                    src_file,
                    os.path.join(WorkPath, itemname, filename)
                )
            else:
                shutil.copytree(
                    src_file,
                    os.path.join(WorkPath, itemname, filename)
                )



if __name__ == '__main__':
    nw = NewWork()
    # nw.create_folder()
    # nw.create_ipynb()
    # nw.ipynb_write()

    # nw.clear_item()
