# logger.py

from _datetime import datetime


class Logger(object):
    DIVIDER_LENGTH = 60

    def __init__(self, active=False):
        self.indentation = 0
        self.active = active

    def log(self, message, relative_indentation_self=0, relative_indentation_next=0):
        self.indentation += relative_indentation_self
        if self.active:
            date = str(datetime.now()) + ': '
            indentation = ''.join(str(x) for x in ['-'] * self.indentation)
            if indentation != '':
                indentation += ' '
            print(date + indentation + message)
        self.indentation += relative_indentation_next

    @staticmethod
    def divider(length=DIVIDER_LENGTH):
        print(''.join(str(x) for x in ['-'] * length))

    @staticmethod
    def line():
        print('')
