#!/usr/local/bin/python
#  move_new_folders.py

from move_new_folders_core import DiskInfo
from move_new_folders_core import FileMover
from space_manager_helpers import Logger

TEST_RUN = False
LOGGING = True

SERIES_PREFIX = 'Series'
SERIES_SOURCE_VOLUMES = [DiskInfo(4, 1)]
SERIES_TARGET_VOLUMES = [DiskInfo(4, 1), DiskInfo(4, 2), DiskInfo(4, 3), DiskInfo(4, 4), DiskInfo(10, 1), ]

MOVIES_PREFIX = 'Movies'
MOVIES_SOURCE_VOLUMES = [DiskInfo(6, 1)]
MOVIES_TARGET_VOLUMES = [DiskInfo(6, 1), DiskInfo(6, 2), DiskInfo(6, 3), DiskInfo(6, 4)]

if __name__ == '__main__':
    file_mover = FileMover(TEST_RUN, Logger(LOGGING))
    file_mover.move_folders(SERIES_PREFIX, SERIES_SOURCE_VOLUMES, SERIES_TARGET_VOLUMES)
    file_mover.move_folders(MOVIES_PREFIX, MOVIES_SOURCE_VOLUMES, MOVIES_TARGET_VOLUMES)
