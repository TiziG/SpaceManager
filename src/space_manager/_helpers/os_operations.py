# os_operations.py

import datetime
import os
from collections import namedtuple
from shutil import move
from stat import ST_CTIME, S_ISDIR
from typing import List

from .logger import Logger
from .._shared_objects import Volume
from ..create_symlinks import create_symlinks

Usage = namedtuple('Usage', 'total used free')


class OsOperations(object):

    @staticmethod
    def get_sub_folders(
            parent_path: str,
            allow_symlinks=False,
            empty_only=False,
            minimum_age: datetime.timedelta = datetime.timedelta(days=0),
            logger=Logger(False)
    ) -> List[str]:
        sub_folders = []
        for filename in os.listdir(parent_path):
            path = os.path.join(parent_path, filename)
            try:
                stats = os.lstat(path)  # get info about the file (don't follow symlinks)
            except EnvironmentError:
                continue  # file vanished or permission error
            else:
                if (
                        (allow_symlinks or S_ISDIR(stats.st_mode))  # symlink allowed or is regular directory
                        and (not empty_only or not os.listdir(path))  # all dirs allowed or is empty
                ):
                    modification_age = (datetime.datetime.now()
                                        - datetime.datetime.fromtimestamp(stats[ST_CTIME]))
                    if modification_age > minimum_age:
                        sub_folders.append(path)
                    else:
                        logger.log('Found a folder but its age (%dmin) is less than %dmin: %s'
                                   % (modification_age.seconds // 60,
                                      minimum_age.seconds // 60,
                                      filename))
        logger.log('Found %d valid sub folder(s) in total' % len(sub_folders))
        return sub_folders

    @staticmethod
    def disk_usage(path: str) -> Usage:
        """Return disk usage statistics about the given path.

        Returned values is a named tuple with attributes 'total', 'used' and
        'free', which are the amount of total, used and free space, in bytes.
        """
        stats = os.statvfs(path)  # pylint: disable=no-member
        free = stats.f_bavail * stats.f_frsize
        total = stats.f_blocks * stats.f_frsize
        used = (stats.f_blocks - stats.f_bfree) * stats.f_frsize
        return Usage(total, used, free)

    @staticmethod
    def get_emptiest_volume(volumes: List[Volume],
                            logger=Logger(False)) -> Volume:
        logger.log('%d possible target volumes. Searching for emptiest...' % len(volumes), 0, 1)
        volume_with_most_free_space = OsOperations.get_emptiest_or_fullest_volume(
            volumes,
            get_fullest=False,
            logger=logger
        )
        logger.log('search for emptiest volume finished', -1)
        return volume_with_most_free_space

    @staticmethod
    def get_fullest_volume(volumes: List[Volume],
                           logger=Logger(False)) -> Volume:
        logger.log('%d possible target volumes. Searching for fullest...' % len(volumes), 0, 1)
        volume_with_most_free_space = OsOperations.get_emptiest_or_fullest_volume(
            volumes,
            get_fullest=True,
            logger=logger
        )
        logger.log('search for fullest volume finished', -1)
        return volume_with_most_free_space

    @staticmethod
    def get_emptiest_or_fullest_volume(
            volumes: List[Volume],
            get_fullest: bool,
            logger=Logger(False)
    ) -> Volume:
        min_max_free_percentage = -1
        min_max_free_volume = None
        for volume in volumes:
            volume_usage = OsOperations.disk_usage(volume.get_absolute_path())
            free_space_in_percent = (100 / volume_usage.total) * volume_usage.free
            logger.log('volume %s: %d%% empty' % (volume.to_string(), free_space_in_percent))
            if (
                    min_max_free_percentage == -1
                    or (get_fullest and free_space_in_percent < min_max_free_percentage)
                    or (not get_fullest and free_space_in_percent > min_max_free_percentage)
            ):
                min_max_free_percentage = free_space_in_percent
                min_max_free_volume = volume
        return min_max_free_volume

    @staticmethod
    def move(
            source: str,
            destination: str,
            stop_sonarr=False,
            create_symlinks_after=False,
            test_run=False,
            logger=Logger(False)
    ):
        OsOperations.move_multiple([source], destination, stop_sonarr, create_symlinks_after, test_run, logger)

    @staticmethod
    def __move(source: str, destination: str, test_run=False, logger=Logger(False)):
        if test_run:
            logger.log('test run: move("%s", "%s")' % (source, destination))
        else:
            logger.log('move("%s", "%s")' % (source, destination))
            if not os.path.exists(destination):
                os.makedirs(destination)
            move(source, destination)

    @staticmethod
    def move_multiple(
            sources: List[str],
            destination: str,
            stop_sonarr=False,
            create_symlinks_after=False,
            test_run=False,
            logger=Logger(False)
    ):
        from .sonarr_api import SonarrApi

        if stop_sonarr:
            SonarrApi.stop_sonarr(test_run, logger)
        for source in sources:
            OsOperations.__move(source, destination, test_run, logger)
        if stop_sonarr:
            SonarrApi.start_sonarr(test_run, logger)
        if create_symlinks_after:
            create_symlinks(test_run, logger)

    @staticmethod
    def remove_directories(
            directories: List[str],
            test_run=False,
            logger=Logger(False)
    ):
        for directory in directories:
            if test_run:
                logger.log("----!!!!---- test run: deleting folder %s ----!!!!---- " % directory)
            else:
                logger.log("----!!!!---- deleting folder %s ----!!!!----" % directory)
                os.rmdir(directory)

    @staticmethod
    def get_tree_size(path: str) -> int:
        """Return total size of files in given path and subdirs."""
        total = 0
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                total += OsOperations.get_tree_size(entry.path)
            else:
                total += entry.stat(follow_symlinks=False).st_size
        return total
