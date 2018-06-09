# distributer.py

from space_manager.smlib.config import DistributerConfig
from space_manager.smlib.helpers import OsOperations
from space_manager.smlib.models import Category, DataFolder
from .check import Check
from .find import Find


class Distributor(object):

    def __init__(self, category: Category, config: DistributerConfig):
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
        """
        Moves all folder in the link-directories of a provided Category to
        the data-directory with the most free space.
        """
        function_name = "distribute_from_link_folders"
        self.__start(function_name)

        folder_name_prefix = self.category.prefix
        source_volumes = self.category.link_source_volumes
        target_volumes = self.category.data_volumes

        self._logger.log('Search in %d source volume(s) for new folders' % len(source_volumes), 0, 1)
        source_folder_paths = Find.subfolders_inside_link_folders(self._config, folder_name_prefix, source_volumes,
                                                                  self._config.minimum_age)
        self._logger.change_indentation(-1)

        if not source_folder_paths:
            self.__end(function_name)
            return

        target_volume = OsOperations.get_emptiest_volume(target_volumes, self._logger)
        self._logger.log('target volume set to: ' + target_volume.to_string())

        OsOperations.move_multiple(
            sources=source_folder_paths,
            destination=DataFolder(target_volume, folder_name_prefix).get_absolute_path(),
            stop_sonarr=self.category.sonarr_related,
            create_symlinks_after=True,
            test_run=self._test_run,
            logger=self._logger
        )

        self.__end(function_name)

    def distribute_from_data_folders(self):
        function_name = "distribute_from_data_folders"
        self.__start(function_name)

        fullest_volume = OsOperations.get_fullest_volume(self.category.data_volumes)
        fullest_usage = OsOperations.disk_usage(fullest_volume.get_absolute_path())
        emptiest_volume = OsOperations.get_emptiest_volume(self.category.data_volumes)
        emptiest_usage = OsOperations.disk_usage(emptiest_volume.get_absolute_path())

        self._logger.log('fullest disk is: %s' % fullest_volume.to_string())
        if not Check.fullest_threshold_met(self._config, fullest_usage):
            self.__end(function_name)
            return

        emptiest_free = emptiest_usage.free
        fullest_free = fullest_usage.free
        self._logger.log('emptiest disk is: %s' % emptiest_volume.to_string())
        if not Check.enough_free_space(self._config, emptiest_free, fullest_free):
            self.__end(function_name)
            return

        self._logger.log('Search for small enough folders', 0, 1)
        folder_to_move = Find.a_folder_small_enough(self._config, emptiest_free, fullest_free,
                                                    DataFolder(fullest_volume, self.category.prefix))
        self._logger.change_indentation(-1)
        if not folder_to_move:
            self.__end(function_name)
            return

        self._logger.log('start moving procedure', 0, 1)
        OsOperations.move(
            source=folder_to_move,
            destination=DataFolder(emptiest_volume, self.category.prefix).get_absolute_path(),
            stop_sonarr=self.category.sonarr_related,
            create_symlinks_after=True,
            test_run=self._test_run,
            logger=self._logger
        )
        self._logger.change_indentation(-1)

        self.__end(function_name)

    def __end(self, name: str):
        self._logger.log_end(self.__get_title_for_log(name))

    def __start(self, name: str):
        self._logger.log_start(self.__get_title_for_log(name))

    def __get_title_for_log(self, name):
        return '%s for %s' % (name, self.category.prefix)
