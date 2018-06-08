# re_distributer.py
import random

from space_manager.shared_objects import DataFolder
from space_manager.helpers import Logger, OsOperations


def b_to_gb(b):  # pylint: disable=invalid-name
    return b / 1_000_000_000


class ReDistributer(object):
    def __init__(self, config, test_run=False, logger=Logger(False)):
        self._test_run = test_run
        self._logger = logger
        self._config = config
        self._logger.divider()
        self._logger.log("initialized Folder deleter with test run set to %s" % str(self._test_run))

    def distribute_from_data_folders(self, category):
        self._logger.divider()
        self._logger.log('start of distribute for ' + category.prefix, 0, 1)

        fullest_volume = OsOperations.get_fullest_volume(category.data_volumes)
        fullest_usage = OsOperations.disk_usage(fullest_volume.get_absolute_path())
        emptiest_volume = OsOperations.get_emptiest_volume(category.data_volumes)
        emptiest_usage = OsOperations.disk_usage(emptiest_volume.get_absolute_path())

        self._logger.log('fullest disk is: %s' % fullest_volume.to_string())

        if not self.__fullest_threshold_met(fullest_usage):
            return

        emptiest_free = emptiest_usage.free
        fullest_free = fullest_usage.free

        self._logger.log('emptiest disk is: %s' % emptiest_volume.to_string())

        if not self.__enough_free_space(emptiest_free, fullest_free):
            return

        folder_to_move = self.__find_folder_to_move(
            emptiest_free,
            fullest_free,
            DataFolder(fullest_volume, category.prefix)
        )
        if not folder_to_move:
            return

        OsOperations.move(
            source=folder_to_move,
            destination=DataFolder(emptiest_volume, category.prefix).get_absolute_path(),
            stop_sonarr=category.sonarr_related,  # pylint: disable=duplicate-code
            create_symlinks_after=True,
            test_run=self._test_run,
            logger=self._logger)

        self._logger.log('End of distribute for ' + category.prefix, -1)
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
