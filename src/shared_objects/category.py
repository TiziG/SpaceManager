# category.py
import shared_objects


class Category(object):
    def __init__(self,
                 prefix,
                 link_source_volumes,
                 data_volumes,
                 sonarr_related=False
                 ):
        self.prefix = prefix
        self.link_source_volumes = link_source_volumes
        self.data_volumes = data_volumes
        self.sonarr_related = sonarr_related

    @property
    def all_folders(self):
        folders = []
        for source_volume in self.link_source_volumes:
            folders.append(shared_objects.LinkFolder(source_volume, self.prefix))
        for data_volume in self.data_volumes:
            folders.append(shared_objects.DataFolder(data_volume, self.prefix))
        return set(folders)
