# root_folder.py
from abc import ABCMeta


class RootFolder(object):
    __metaclass__ = ABCMeta

    def __init__(self, volume, prefix):
        self.volume = volume
        self.prefix = prefix

    def get_absolute_path(self):
        return self.volume.get_absolute_path() + self.prefix
