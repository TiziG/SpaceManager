# root_folder.py

from abc import ABCMeta

from .volume import Volume


class RootFolder(object):
    __metaclass__ = ABCMeta

    def __init__(self, volume: Volume, prefix: str):
        self.volume = volume
        self.prefix = prefix

    def get_absolute_path(self) -> str:
        return self.volume.get_absolute_path() + self.prefix

    def key(self):
        return self.prefix, self.volume

    def __eq__(self, other):
        return self.key() == other.key()

    def __hash__(self):
        return hash(self.key())


class DataFolder(RootFolder):
    def get_absolute_path(self) -> str:
        return (super(DataFolder, self).get_absolute_path()
                + self.volume.disk_info.to_string(is_link_target=True))


class LinkFolder(RootFolder):
    def get_absolute_path(self) -> str:
        return (super(LinkFolder, self).get_absolute_path()
                + self.volume.disk_info.to_string(is_link_target=False))
