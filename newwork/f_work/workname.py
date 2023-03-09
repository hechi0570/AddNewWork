from datetime import datetime

class WorkName:
    '''管理项目名'''
    def __init__(self) -> None:
        self._today: str = datetime.today().strftime('%y%m%d')

    @property
    def name(self):
        return self._today

