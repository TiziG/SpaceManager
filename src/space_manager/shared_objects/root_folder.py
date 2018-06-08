# root_folder.py
from abc import ABCMeta


class RootFolder(object):
    __metaclass__ = ABCMeta

    def __init__(self, volume, prefix):
        self.volume = volume
        self.prefix = prefix

    def get_absolute_path(self):
        return self.volume.get_absolute_path() + self.prefix

    def __key(self):
        return self.prefix, self.volume

    def __eq__(self, other):
        return self.__key() == other.key()

    def __hash__(self):
        return hash(self.__key())


class DataFolder(RootFolder):
    def get_absolute_path(self):
        return (super(DataFolder, self).get_absolute_path()
                + self.volume.disk_info.to_string(is_link_target=True))


class LinkFolder(RootFolder):
    def get_absolute_path(self):
        return (super(LinkFolder, self).get_absolute_path()
                + self.volume.disk_info.to_string(is_link_target=False))
