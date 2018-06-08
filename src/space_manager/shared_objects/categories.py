# categories.py

class Categories(object):
    def __init__(self, categories):
        self.categories = categories

    @property
    def all_folders(self):
        folders = []
        for category in self.categories:
            folders.extend(category.all_folders)
        return set(folders)
