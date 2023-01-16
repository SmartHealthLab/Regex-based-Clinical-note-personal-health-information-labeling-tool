from datetime import datetime


DATE_FORMAT_STRING = '%Y-%m-%d %H:%M:%S'


class Elapsed:
    def __init__(self, name=None) -> None:
        self._name = name
        self._start = datetime.now()
        self.print_start(name)
        
    def print_start(self, msg='') -> None:
        print('============================================================')
        print(f'{self._start.strftime(DATE_FORMAT_STRING)} start: {msg}')
        print('============================================================')

    def print_elapsed(self, msg='') -> None:
        current = datetime.now()
        print('============================================================')
        print(f'{current.strftime(DATE_FORMAT_STRING)} elapsed: {self._name}: {current - self._start}: {msg}')
        print('============================================================')