# link_folder.py
from shared_objects import RootFolder


class LinkFolder(RootFolder):
    def get_absolute_path(self):
        return (
                super(LinkFolder, self).get_absolute_path()
                + self.volume.disk_info.to_string(is_link_target=False)
        )
