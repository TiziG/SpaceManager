#!/usr/local/bin/python
#  move_new_folders.py

import datetime

from config import CategoryAndVolumeDefinitions
from move_new_folders_core import FileMover
from space_manager_helpers import Logger

# configuration-----------
TEST_RUN = False
LOGGING = True
MINIMUM_AGE = datetime.timedelta(hours=5)
# ------------------------

if __name__ == '__main__':
    file_mover = FileMover(TEST_RUN, Logger(LOGGING))
    for category in CategoryAndVolumeDefinitions.categories.categories:
        file_mover.move_folders(category, MINIMUM_AGE)
