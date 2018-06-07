# categories.py

class Categories(object):
    def __init__(self, categories):
        self.categories = categories

    @property
    def all_volumes(self):
        volumes = []
        for category in self.categories:
            volumes.extend(category.all_volumes)
        return set(volumes)
