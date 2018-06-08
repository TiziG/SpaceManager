# category.py

from typing import List, Set

from .root_folder import DataFolder, LinkFolder, RootFolder
from .volume import Volume


class Category(object):
    def __init__(
            self,
            prefix: str,
            link_source_volumes: List[Volume],
            data_volumes: List[Volume],
            sonarr_related=False
    ):
        self.prefix = prefix
        self.link_source_volumes = link_source_volumes
        self.data_volumes = data_volumes
        self.sonarr_related = sonarr_related

    @property
    def all_folders(self) -> Set[RootFolder]:
        folders = []
        for source_volume in self.link_source_volumes:
            folders.append(LinkFolder(source_volume, self.prefix))
        for data_volume in self.data_volumes:
            folders.append(DataFolder(data_volume, self.prefix))
        return set(folders)
