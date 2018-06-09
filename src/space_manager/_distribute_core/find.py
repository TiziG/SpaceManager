import random
from typing import List

from space_manager._config import DistributerConfig
from space_manager._helpers import Converter, OsOperations
from space_manager._shared_objects import DataFolder, LinkFolder, Volume


class Find(object):
    @staticmethod
    def subfolders_inside_link_folders(config: DistributerConfig, folder_name_prefix: str,
                                       source_volumes: List[Volume], minimum_age) -> List[str]:
        folder_paths = []
        for source_volume in source_volumes:
            folder_paths.extend(
                OsOperations.get_sub_folders(
                    parent_path=LinkFolder(source_volume, folder_name_prefix).get_absolute_path(),
                    allow_symlinks=False,
                    minimum_age=minimum_age,
                    logger=config.logger
                )
            )
        return folder_paths

    @staticmethod
    def a_folder_small_enough(config: DistributerConfig, emptiest_free: int, fullest_free,
                              parent_folder: DataFolder) -> str:
        max_movable_size = (emptiest_free - fullest_free) / 2
        config.logger.log("Max folder size to be considered: %dGB" %
                          Converter.b_to_gb(max_movable_size))
        possible_folders = [
            folder for
            folder in OsOperations.get_sub_folders(parent_folder.get_absolute_path())
            if OsOperations.get_tree_size(folder) < max_movable_size
        ]
        config.logger.log("%d folders meet criteria" % len(possible_folders))
        if not possible_folders:
            return ''
        folder_to_move = random.choice(possible_folders)
        config.logger.log("choosing a random folder (%dGB): %s" %
                          (Converter.b_to_gb(OsOperations.get_tree_size(folder_to_move)),
                           folder_to_move))
        return folder_to_move
