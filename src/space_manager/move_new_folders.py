#!/usr/local/bin/python
#  move_new_folders.py

import datetime

from space_manager.config import CategoryAndVolumeDefinitions
from space_manager.distribute_core import Distributer
from space_manager.helpers import Logger

# configuration-----------
TEST_RUN = False
LOGGING = True
MINIMUM_AGE = datetime.timedelta(hours=5)
# ------------------------

if __name__ == '__main__':
    FILE_MOVER = Distributer(TEST_RUN, Logger(LOGGING))
    for category in CategoryAndVolumeDefinitions.categories.categories:
        FILE_MOVER.distribute_from_link_folders(category, MINIMUM_AGE)
