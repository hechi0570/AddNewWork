import sys
sys.path.append('..')

import os
import PySimpleGUI as sg

from f_work import MyItem
from gui_e import except_

sg.set_options(font=('微软雅黑', 9))
sg.theme('LightGrey1')


file_layout = [
    [sg.Text('接收文件')],
    [
        sg.Listbox('', select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, size=(
            30, 20), horizontal_scroll=True, key='-wxfolder-')
    ],
    [
        sg.FolderBrowse('选择文件夹', tooltip='选择接收文件的目录',
                        change_submits=True, enable_events=False, key='-folder-'),
        sg.Input(size=(25, 1), disabled=True,
                 enable_events=True, key='-folderpath-'),
    ]
]

itemfile_layout = [
    [sg.Text('项目文件')],
    [
        sg.Listbox('', size=(
            30, 20), horizontal_scroll=True, key='-itemfolder-')
    ]
]

but_layout = [
    [sg.Text(key='-msg-')],
    [sg.ButtonMenu('新建项目', ['', ['默认名称::_default_', '自定义名称::-custom-']],
                   key='Menu::NewItem', tooltip='新建项目的选项')],
    [sg.Button('复制项目文件', key='-copyitemfiles-')],
    [sg.ButtonMenu(
        '项目管理', ['', ['打开项目::-openitem-', '清除项目::_clearitem_']], key='Menu::manageitem')]
]

# but_fr = sg.Frame('', layout=but_layout, vertical_alignment='top')

layout = [
    [
        sg.Column(file_layout, vertical_alignment='top'),
        sg.Column(itemfile_layout, vertical_alignment='top'),
        sg.Column(but_layout, vertical_alignment='top', expand_y=True, ),
    ]
]

def init_window(window: sg.Window):
    window['-wxfolder-'].update(values=list('ABCDE'))

def new_item(item_name: str = ''):
    MyItem(fname=item_name).add()

window = sg.Window('NewWork', layout, size=(800, 600), finalize=True)
init_window(window)
# input()

while True:
    event, values = window.read()
    if event in (None, ):
        break
    print('event ->', event)
    print('values ->', values)
    except_(event=event, values=values)

window.close()