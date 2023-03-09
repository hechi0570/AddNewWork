import PySimpleGUI as sg
import os
from add_new_work import NewWork, WorkPath

nw = NewWork()

sg.set_options(font=('微软雅黑', 9))
sg.theme('LightGrey1')


file_layout = [
    [sg.Text('接收文件')],
    [
        sg.Listbox(nw.show_item_files(path=nw.wx_path, only_path=True), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED, size=(
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
        sg.Listbox(nw.show_item_files(path=WorkPath), size=(
            30, 20), horizontal_scroll=True, key='-itemfolder-')
    ]
]

but_layout = [
    [sg.Text(key='-msg-')],
    [sg.ButtonMenu('新建项目', ['', ['默认名称::-default-', '自定义名称::-custom-']],
                   key='-BM-', tooltip='新建项目的选项')],
    [sg.Button('复制项目文件', key='-copyitemfiles-')],
    [sg.ButtonMenu(
        '项目管理', ['', ['打开项目::-openitem-', '清除项目::-clearitem-']], key='-manageitem-')]
]

# but_fr = sg.Frame('', layout=but_layout, vertical_alignment='top')

layout = [
    [
        sg.Column(file_layout, vertical_alignment='top'),
        sg.Column(itemfile_layout, vertical_alignment='top'),
        sg.Column(but_layout, vertical_alignment='top', expand_y=True, ),
    ]
]

window = sg.Window('NewWork', layout, size=(800, 600))

while True:
    event, values = window.read()
    if event in (None, ):
        break
    # elif event == '-BM-':
    print(event, '\n', values)
    if event == '-BM-':
        if values.get('-BM-').endswith('-default-'):
            print('1'*100)
            try:
                nw.create_folder()
                nw.create_ipynb()
                window['-itemfolder-'].update(
                    nw.show_item_files(path=WorkPath))
                window['-msg-'].update('项目文件夹创建完成')
            except FileExistsError:
                sg.popup_error('项目已存在')

        elif values.get('-BM-').endswith('-custom-'):
            item_name = sg.popup_get_text(
                '输入项目名称', '项目名称', default_text='施工中...')
            print(item_name)

    elif event == '-copyitemfiles-':
        print(values.get('-wxfolder-'))
        try:
            nw.copy_item_flies(values.get('-wxfolder-'), is_gui=True)
            window['-itemfolder-'].update(nw.show_item_files(path=WorkPath))
        except FileNotFoundError:
            sg.popup_error('需要先创建项目文件夹')

    elif event == '-manageitem-':
        manage_v: str = values['-manageitem-']
        if manage_v.endswith('-clearitem-'):
            del_msg = sg.popup_yes_no('清除项目会删除所有的项目相关文件')
            if del_msg == 'Yes':
                try:
                    nw.clear_item()
                    window['-itemfolder-'].update(
                        nw.show_item_files(path=WorkPath))
                    window['-msg-'].update('项目文件已清除')
                except FileNotFoundError:
                    pass
        if manage_v.endswith('-openitem-'):
            # webbrowser.open(os.path.join(nw.work_path, nw.today))
            try:
                os.startfile(os.path.join(nw.work_path, nw.today))
            except FileNotFoundError:
                sg.popup('没有项目文件夹')

    elif event == '-folderpath-':
        print('folder', values['-folder-'])
        window['-wxfolder-'].update(nw.show_item_files(
            path=values.get('-folderpath-'), only_path=True))
        nw.wx_path = values.get('-folderpath-')


window.close()
