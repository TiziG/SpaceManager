# disk_info.py

class DiskInfo(object):
    def __init__(self, terra_byte: int, version=1):
        self.terra_byte = terra_byte
        self.version = version

    def to_string(self, is_link_target=False) -> str:
        if is_link_target:
            version_data = 'D'
        else:
            version_data = 'V'
        return str(self.terra_byte) + 'TB-' + version_data + str(self.version)

    def key(self):
        return self.terra_byte, self.version

    def __eq__(self, other):
        return self.key() == other.key()

    def __hash__(self):
        return hash(self.key())
