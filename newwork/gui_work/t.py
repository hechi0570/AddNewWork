import PySimpleGUI as sg
sg.theme('LightGrey1')

# GLOBALS

LIST_FILMS = ['The Dead Zone', 'Frailty', 'Shutter Island']

# CLASSES


class Model():

    def __init__(self):
        self.list = LIST_FILMS

    @property
    def names(self):
        return self.list

    def delete_by_index(self, index):
        self.list.pop(index)

    def add(self, name):
        self.list.append(name)


class View():

    def __init__(self, window, layout):

        # general
        self.w = window
        self.l = layout

        # local
        self.key = None
        self.values = None

    def update(self, event, values):
        self.key = event
        self.values = values

    def refresh(self, model):
        self.element('-LIST-').update(values=model.names)
        self.element('-NAME-').update(value='')

    # ----key element
    def element(self, key):
        return self.w[key]

    def value(self, key):
        return self.values.get(key)

    def show(self, key):
        self.w[key].update(visible=True)

    def hide(self, key):
        self.w[key].update(visible=False)

    def index_selected_list(self, key):
        return self.element(key).GetIndexes()[0]

    # ----current element
    @property
    def __element(self):
        if self.key != '__TIMEOUT__':
            return self.w[self.key]
        else:
            return None


class Controller():

    def __init__(self, model, view):
        self.m = model
        self.v = view
        self._index_selected = None
        self._modifying_list = False

    def update(self, event):

        if event == '-LIST-':
            if self.v.index_selected_list('-LIST-') == self._index_selected:
                self.v.refresh(self.m)
                self._index_selected = None
            else:
                self.v.element(
                    '-NAME-').update(value=self.v.value('-LIST-')[0])
                self._index_selected = self.v.index_selected_list('-LIST-')
                self._modifying_list = True

        if event == '-ADD-':
            if self.v.value('-NAME-'):
                self.m.add(self.v.value('-NAME-'))
                self.v.refresh(model=self.m)
                self._modifying_list = False
                self._index_selected = None

        if event == '-DELETE-':
            if self._index_selected:
                self.m.delete_by_index(int(self._index_selected))
                self.v.refresh(model=self.m)
                self._modifying_list = False
                self._index_selected = None

        if self.v.value('-NAME-') != '':
            self._modifying_list = True
        else:
            self._modifying_list = False

        if self._modifying_list:
            self.v.show('-ADD-')
            self.v.show('-DELETE-')
        else:
            self.v.hide('-ADD-')
            self.v.hide('-DELETE-')

# METHODS


def main():

    # Model
    m = Model()

    # GUI
    layout = [[sg.Listbox(values=m.names, size=(20, 6), key='-LIST-', select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, enable_events=True)],
              [sg.Text('Name: ', size=(15, 1)), sg.InputText(key='-NAME-')],
              [sg.Button('Add', key='-ADD-', visible=False),
               sg.Button('Delete', key='-DELETE-', visible=False)],
              [sg.Button('Exit')]]

    window = sg.Window('Movie Listbox', layout,
                       grab_anywhere=False, finalize=True)

    # View
    v = View(window, layout)

    # Controller
    c = Controller(m, v)

    # Polling
    while True:

        event, values = window.read(timeout=100)

        if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
            break

        # update of the view parameters (can be included in controller)
        v.update(event, values)

        # update of controller
        c.update(event)

        # more if statements not involving models/view (for exemple trigger new windows ...)

    window.close()
    return m

# MAIN


if __name__ == '__main__':
    model = main()
