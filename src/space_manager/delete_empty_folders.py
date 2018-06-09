#!/usr/local/bin/python
#  delete_empty_folders.py

import datetime

from space_manager.config import CATEGORY_COLLECTION
from space_manager.delete_empty_folders_core import FolderDeleter
from space_manager.helpers import Logger

# configuration-----------
TEST_RUN = False
LOGGING = True
MINIMUM_AGE = datetime.timedelta(hours=1)
# ------------------------

if __name__ == '__main__':
    FOLDER_DELETER = FolderDeleter(TEST_RUN, Logger(LOGGING))
    for folder in CATEGORY_COLLECTION.all_folders:
        FOLDER_DELETER.delete_empty_folders(folder, MINIMUM_AGE)
