import sys
sys.path.append('..')

from f_work import MyItem

ORDERS = {
    '-default-': MyItem
}

class E:
    def __init__(self, event: str, values: str):
        self.event = event
        self.values = values

    def type_menu(self):
        if self.event.startswith('Menu'):
            value = self.values.get(self.event)
            self.key = value.split('::')[-1]
        else:
            self.key = self.event
    
    def orders(self):
        if self.key == '_default_':
            MyItem().add()
        elif self.key == '_clearitem_':
            MyItem().remove()


def except_(event, values):
    e = E(event, values)
    e.type_menu()
    e.orders()

    
