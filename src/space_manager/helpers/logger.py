# logger.py

from _datetime import datetime


class Logger(object):
    DIVIDER_LENGTH = 60

    def __init__(self, active=False):
        self._indentation = 0
        self._active = active

    def log(self, message: str, relative_indentation_self=0, relative_indentation_next=0):
        self._indentation += relative_indentation_self
        if self._active:
            date = str(datetime.now()) + ': '
            indentation = ''.join(str(x) for x in ['-'] * self._indentation)
            if indentation != '':
                indentation += ' '
            print(date + indentation + message)
        self._indentation += relative_indentation_next

    def change_indentation(self, increment: int):
        self._indentation += increment

    @staticmethod
    def divider(length=DIVIDER_LENGTH):
        print(''.join(str(x) for x in ['-'] * length))

    @staticmethod
    def line():
        print('')

    def log_condition(self, result: bool):
        if result:
            self.log("condition met")
        else:
            self.log("condition not met")

    def log_start(self, title: str):
        self.divider()
        self.log('Start of %s' % title, 0, 1)

    def log_end(self, title: str):
        self.log('End of %s' % title, -1)
        self.divider()
