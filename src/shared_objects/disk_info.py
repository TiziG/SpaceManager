# disk_info.py

class DiskInfo(object):
    def __init__(self, tb, version=1):
        self.tb = tb
        self.version = version

    def to_string(self, is_link_target=False):
        if is_link_target:
            version_data = 'D'
        else:
            version_data = 'V'
        return str(self.tb) + 'TB-' + version_data + str(self.version)

    def __key(self):
        return self.tb, self.version

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())
