# data_folder.py
from shared_objects import RootFolder


class DataFolder(RootFolder):
    def get_absolute_path(self):
        return (
                super(DataFolder, self).get_absolute_path()
                + self.volume.disk_info.to_string(is_link_target=True)
        )
