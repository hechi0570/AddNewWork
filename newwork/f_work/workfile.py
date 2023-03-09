import os
import webbrowser
import shutil
from .workname import WorkName
from .new_txt_file import NewIpynb

IpynbPath = 'D:/'
WorkPath = 'D:/'

class IpynbFile:
    '''用于建立 jupyter 文件'''
    def __init__(self, fname: str):
        self.fname = fname

    def create_ipynb(self, date: str = None):
        '''建立 jupyter 文件'''
        if date is None:
            date = self.fname
        self.filename = f'{date}.ipynb'
        file_path = os.path.join(IpynbPath, self.filename)

        if self.filename in os.listdir(IpynbPath):
            raise FileExistsError

        with open(file_path, 'w') as f:
            f.write(NewIpynb(file_path=IpynbPath, file_name=self.fname).create())
        print('ipynb 文件创建成功')


    def remove(self):
        try:
            os.remove(os.path.join(IpynbPath, f'{self.fname}.ipynb'))   
        except Exception as e:
            print(f'{e} -> ipynb 删除失败')


class Folder:
    def __init__(self, fname: str):
        self.fname = fname

    def create_folder(self, date: str = None):
        '''建立工作目录'''
        if date is None:
            date = self.fname
        try:
            os.mkdir(os.path.join(WorkPath, date))
        except FileExistsError:
            raise FileExistsError
        print('工作目录创建成功') 

    def remove(self):
        try:
            shutil.rmtree(os.path.join(WorkPath, self.fname))
        except Exception as e:
            print(f'{e} -> folder 删除失败')

    def open_(self):
        '''打开项目文件夹'''
        path = os.path.join(WorkPath, self.fname)
        if os.path.isdir(path):
            webbrowser.open(path)
        else:
            raise FileNotFoundError