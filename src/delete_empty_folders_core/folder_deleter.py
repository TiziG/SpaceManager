# folder_deleter.py

from space_manager_helpers import Logger, OsOperations


class FolderDeleter(object):
    VOLUME_PREFIX = 'Data'
    MOUNT_POINT = r'/mnt/'

    def __init__(self, test_run=False, logger=Logger(False)):
        self._test_run = test_run
        self._logger = logger

    def delete_empty_folders(self, volume, minimum_age):
        OsOperations.remove_empty_sub_directories(
            volume.get_absolute_path(),
            minimum_age=minimum_age,
            logger=self._logger
        )
