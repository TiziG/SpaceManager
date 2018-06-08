# distributer.py

import random

from space_manager.config import DistributerConfig
from space_manager.helpers import OsOperations
from space_manager.shared_objects import LinkFolder, DataFolder


def b_to_gb(b):  # pylint: disable=invalid-name
    return b / 1_000_000_000


class Distributer(object):

    def __init__(self, category, config: DistributerConfig):
        self.category = category
        self._config = config
        self._logger.divider()
        self._logger.log("initialized Distributer with test run set to %s" % str(self._test_run))

    @property
    def _logger(self):
        return self._config.logger

    @property
    def _test_run(self):
        return self._config.test_run

    def distribute_from_link_folders(self):
        """ Moves all folder in the link-directories of a provided Category to
            the data-directory with the most free space.
            Parameters
            minimum_age: move only folders older than this
        """
        folder_name_prefix = self.category.prefix
        source_volumes = self.category.link_source_volumes
        target_volumes = self.category.data_volumes

        self._logger.divider()
        self._logger.log('start of main function for ' + folder_name_prefix, 0, 1)
        self._logger.log('test run is set to %s' % str(self._test_run))

        self._logger.log('Search in %d source volume(s) for new folders'
                         % len(source_volumes), 0, 1)
        source_folder_paths = self.__get_folder_paths_to_move(folder_name_prefix,
                                                              source_volumes,
                                                              self._config.minimum_age)
        self._logger.change_indentation(-1)

        if not source_folder_paths:
            self.__end()
            return

        target_volume = OsOperations.get_emptiest_volume(target_volumes, self._logger)
        self._logger.log('target volume set to: ' + target_volume.to_string())

        OsOperations.move_multiple(sources=source_folder_paths,
                                   destination=DataFolder(target_volume, folder_name_prefix).get_absolute_path(),
                                   stop_sonarr=self.category.sonarr_related,
                                   create_symlinks_after=True,
                                   test_run=self._test_run,
                                   logger=self._logger)

        self.__end()

    def distribute_from_data_folders(self):
        self._logger.divider()
        self._logger.log('start of distribute for ' + self.category.prefix, 0, 1)

        fullest_volume = OsOperations.get_fullest_volume(self.category.data_volumes)
        fullest_usage = OsOperations.disk_usage(fullest_volume.get_absolute_path())
        emptiest_volume = OsOperations.get_emptiest_volume(self.category.data_volumes)
        emptiest_usage = OsOperations.disk_usage(emptiest_volume.get_absolute_path())

        self._logger.log('fullest disk is: %s' % fullest_volume.to_string())

        if not self.__fullest_threshold_met(fullest_usage):
            return

        emptiest_free = emptiest_usage.free
        fullest_free = fullest_usage.free

        self._logger.log('emptiest disk is: %s' % emptiest_volume.to_string())

        if not self.__enough_free_space(emptiest_free, fullest_free):
            return

        folder_to_move = self.__find_folder_to_move(emptiest_free,
                                                    fullest_free,
                                                    DataFolder(fullest_volume, self.category.prefix))
        if not folder_to_move:
            return

        OsOperations.move(source=folder_to_move,
                          destination=DataFolder(emptiest_volume, self.category.prefix).get_absolute_path(),
                          stop_sonarr=self.category.sonarr_related,
                          create_symlinks_after=True,
                          test_run=self._test_run,
                          logger=self._logger)

        self.__end()

    def __end(self):
        self._logger.log('End of distribute for ' + self.category.prefix, -1)
        self._logger.divider()

    def __find_folder_to_move(self, emptiest_free, fullest_free, parent_folder: DataFolder):
        max_movable_size = (emptiest_free - fullest_free) / 2
        self._logger.log("Max folder size to be considered for moving: %dGB" %
                         b_to_gb(max_movable_size))
        possible_folders = [folder for
                            folder in OsOperations.get_sub_folders(parent_folder.get_absolute_path())
                            if OsOperations.get_tree_size(folder) < max_movable_size]
        self._logger.log("%d folders meet criteria" % len(possible_folders))
        if not possible_folders:
            self.__condition_not_met()
            return False
        folder_to_move = random.choice(possible_folders)
        self._logger.log("choosing folder (%dGB): %s" %
                         (b_to_gb(OsOperations.get_tree_size(folder_to_move)), folder_to_move))
        return folder_to_move

    def __enough_free_space(self, emptiest_free, fullest_free):
        minimum_free_needed = fullest_free * 2
        self._logger.log("Free space needed to start algorithm: %dGB" % (
            b_to_gb(minimum_free_needed)))
        self._logger.log("actual free space: %dGB" % (
            b_to_gb(emptiest_free)))
        if emptiest_free < minimum_free_needed:
            self.__condition_not_met()
            return False
        self._logger.log("condition met, continuing...")
        return True

    def __fullest_threshold_met(self, fullest_usage):
        fullest_used = fullest_usage.used / fullest_usage.total
        self._logger.log("The Fullest disk is at %d%%. Threshold is %d%%" % (
            fullest_used * 100, self._config.fullest_threshold * 100))
        if fullest_used < self._config.fullest_threshold:
            self.__condition_not_met()
            return False
        self._logger.log("condition met, continuing...")
        return True

    def __condition_not_met(self):
        self._logger.log("condition not met. ending.", -1)
        self._logger.divider()

    def __get_folder_paths_to_move(self, folder_name_prefix, source_volumes, minimum_age):
        folder_paths = []
        for source_volume in source_volumes:
            folder_paths.extend(OsOperations.get_sub_folders(
                    parent_path=LinkFolder(source_volume, folder_name_prefix).get_absolute_path(),
                    allow_symlinks=False,
                    minimum_age=minimum_age,
                    logger=self._logger))
        return folder_paths
