#!/usr/local/bin/python
#  delete_empty_folders.py

import datetime

from space_manager._config import CATEGORY_COLLECTION
from space_manager._delete_empty_folders_core import FolderDeleter
from space_manager._helpers import Logger

# configuration-----------
TEST_RUN = False
LOGGING = True
MINIMUM_AGE = datetime.timedelta(hours=1)


# ------------------------

def delete_empty_folders():
    folder_deleter = FolderDeleter(TEST_RUN, Logger(LOGGING))
    for folder in CATEGORY_COLLECTION.all_folders:
        folder_deleter.delete_empty_folders(folder, MINIMUM_AGE)
