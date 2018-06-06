# logger.py

class Logger(object):
    def __init__(self, active=False):
        self.indentation = 0
        self.active = active

    def log(self, message, relative_indentation=0):
        self.indentation += relative_indentation
        if self.active:
            print('-'.join(str(x) for x in [''] * self.indentation) + message)