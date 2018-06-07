# file_mover.py

from create_symlinks import create_symlinks
from shared_objects import LinkFolder, DataFolder
from space_manager_helpers import Logger, OsOperations, SonarrApi


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

        target_volume = OsOperations.get_volume_with_most_free_space(target_volumes, self._logger)
        self._logger.log('target volume set to: ' + target_volume.to_string())

        self._logger.log('Search in %d source volume(s) for new folders' % len(source_volumes), 0, 1)
        source_folder_paths = self.__get_folder_paths_to_move(folder_name_prefix, source_volumes, minimum_age)

        if source_folder_paths:
            SonarrApi.stop_sonarr(self._test_run, self._logger)
            for path in source_folder_paths:
                OsOperations.move(
                    path,
                    DataFolder(target_volume, folder_name_prefix).get_absolute_path(),
                    self._test_run,
                    self._logger
                )
            create_symlinks(self._test_run, self._logger)
            SonarrApi.start_sonarr(self._test_run, self._logger)

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
