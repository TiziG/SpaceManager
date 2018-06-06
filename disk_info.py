# disk_info.py

class DiskInfo(object):
    def __init__(self, tb, version=1):
        self.tb = tb
        self.version = version

    def to_string(self, is_link_target):
        if is_link_target:
            version_data = 'D'
        else:
            version_data = 'V'
        return str(self.tb) + 'TB-' + version_data + str(self.version)