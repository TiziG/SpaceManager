# categories.py

from typing import List, Set

from .category import Category
from .root_folder import RootFolder


class Categories(object):
    def __init__(self, categories: List[Category]):
        self.categories = categories

    @property
    def all_folders(self) -> Set[RootFolder]:
        folders = []
        for category in self.categories:
            folders.extend(category.all_folders)
        return set(folders)
