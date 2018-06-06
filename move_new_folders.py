# move_new_folders.py

from file_mover import FileMover
from disk_info import DiskInfo
from logger import Logger

TEST_RUN = True
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
