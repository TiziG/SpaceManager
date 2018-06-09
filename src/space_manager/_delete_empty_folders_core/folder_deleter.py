# folder_deleter.py

import datetime

from space_manager._helpers import Logger, OsOperations
from space_manager._shared_objects import RootFolder


class FolderDeleter(object):
    VOLUME_PREFIX = 'Data'
    MOUNT_POINT = r'/mnt/'

    def __init__(self, test_run=False, logger=Logger(False)):
        self._test_run = test_run
        self._logger = logger
        self._logger.divider()
        self._logger.log("initialized Folder deleter with test run set to %s" % str(self._test_run))

    def delete_empty_folders(self, folder: RootFolder, minimum_age: datetime.timedelta):
        self._logger.divider()
        self._logger.log("start of delete_empty_folders in %s" % folder.get_absolute_path(), 0, 1)
        self._logger.log("start search for empty directories", 0, 1)
        empty_directories = OsOperations.get_sub_folders(
            parent_path=folder.get_absolute_path(),
            empty_only=True,
            minimum_age=minimum_age,
            logger=self._logger
        )
        self._logger.log("end search for empty directories. Found %d" % len(empty_directories), -1)
        OsOperations.remove_directories(
            directories=empty_directories,
            test_run=self._test_run,
            logger=self._logger
        )
        self._logger.log("end of delete_empty_folders", -1)
        self._logger.divider()
