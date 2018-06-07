#!/usr/local/bin/python
#  delete_empty_folders.py
import datetime

from config import CategoryAndVolumeDefinitions
from delete_empty_folders_core import FolderDeleter
from space_manager_helpers import Logger

# configuration-----------
TEST_RUN = False
LOGGING = True
MINIMUM_AGE = datetime.timedelta(hours=1)
# ------------------------

if __name__ == '__main__':
    folder_deleter = FolderDeleter(TEST_RUN, Logger(LOGGING))
    for folder in CategoryAndVolumeDefinitions.categories.all_folders:
        folder_deleter.delete_empty_folders(folder, MINIMUM_AGE)
