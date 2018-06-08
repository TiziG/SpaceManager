# volume.py
from .disk_info import DiskInfo


class Volume(object):
    def __init__(self, mount_point, prefix, disk_info: DiskInfo):
        self.mount_point = mount_point
        self.disk_info = disk_info
        self.prefix = prefix

    def get_absolute_path(self):
        return self.mount_point + self.prefix + self.disk_info.to_string() + '/'

    def to_string(self):
        return self.prefix + self.disk_info.to_string()

    def __key(self):
        return self.mount_point, self.disk_info, self.prefix

    def __eq__(self, other):
        return self.__key() == other.key()

    def __hash__(self):
        return hash(self.__key())
