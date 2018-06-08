# file_mover.py

from shared_objects import LinkFolder, DataFolder
from space_manager_helpers import Logger, OsOperations


class FileMover(object):
    def __init__(self, test_run=False, logger=Logger(False)):
        self._test_run = test_run
        self._logger = logger

    def move_folders(self, category, minimum_age):
        folder_name_prefix = category.prefix
        source_volumes = category.link_source_volumes
        target_volumes = category.data_volumes

        self._logger.divider()
        self._logger.log('start of main function for ' + folder_name_prefix, 0, 1)
        self._logger.log('test run is set to %s' % str(self._test_run))

        self._logger.log('Search in %d source volume(s) for new folders' % len(source_volumes), 0, 1)
        source_folder_paths = self.__get_folder_paths_to_move(folder_name_prefix, source_volumes, minimum_age)

        if not source_folder_paths:
            self.__end()
            return

        target_volume = OsOperations.get_emptiest_volume(target_volumes, self._logger)
        self._logger.log('target volume set to: ' + target_volume.to_string())

        OsOperations.move_multiple(
            sources=source_folder_paths,
            destination=DataFolder(target_volume, folder_name_prefix).get_absolute_path(),
            stop_sonarr=category.sonarr_related,
            create_symlinks_after=True,
            test_run=self._test_run,
            logger=self._logger
        )

        self.__end()

    def __end(self):
        self._logger.log('end of main function', -1)
        self._logger.divider()

    def __get_folder_paths_to_move(self, folder_name_prefix, source_volumes, minimum_age):
        folder_paths = []
        for source_volume in source_volumes:
            folder_paths.extend(
                OsOperations.get_sub_folders(
                    parent_path=LinkFolder(source_volume, folder_name_prefix).get_absolute_path(),
                    allow_symlinks=False,
                    minimum_age=minimum_age,
                    logger=self._logger
                )
            )
        return folder_paths
