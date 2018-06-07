# category.py

class Category(object):
    def __init__(self,
                 prefix,
                 link_source_volumes,
                 data_volumes,
                 ):
        self.prefix = prefix
        self.link_source_volumes = link_source_volumes
        self.data_volumes = data_volumes

    @property
    def all_volumes(self):
        volumes = []
        volumes.extend(self.link_source_volumes)
        volumes.extend(self.data_volumes)
        return set(volumes)
