import webbrowser
import os
from .workfile import IpynbFile, Folder
from .workname import WorkName
from . import *

ITEM_NAME = WorkName().name
class MyItem:
    def __init__(self, fname = None) -> None:
        self._fname = fname
        if fname in (None, ''):
            self._fname = ITEM_NAME
        self._ipynb_file = IpynbFile(fname=self._fname)
        self._folder = Folder(fname=self._fname)
    
    def add(self):
        # 文件和文件夹需要一起创建
        try:
            self._ipynb_file.create_ipynb()
            self._folder.create_folder()
        except Exception as e:
            print(f'{e}aa')

    def remove(self):
        self._ipynb_file.remove()
        self._folder.remove()

    def open_folder(self):
        '''打开项目文件夹'''
        self._folder.open_()
    