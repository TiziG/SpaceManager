# os_operations.py

import datetime
import os
from collections import namedtuple
from shutil import move
from stat import S_ISDIR, ST_CTIME
from typing import List

from create_symlinks import create_symlinks
from shared_objects import Volume
from space_manager_helpers import Logger


class OsOperations(object):

    @staticmethod
    def get_sub_folders(
            parent_path,
            allow_symlinks=False,
            empty_only=False,
            minimum_age: datetime.timedelta = datetime.timedelta(days=0),
            logger=Logger(False)
    ):
        sub_folders = []
        for filename in os.listdir(parent_path):
            path = os.path.join(parent_path, filename)
            try:
                st = os.lstat(path)  # get info about the file (don't follow symlinks)
            except EnvironmentError:
                continue  # file vanished or permission error
            else:
                if (
                        (allow_symlinks or S_ISDIR(st.st_mode))  # symlink allowed or is regular directory
                        and (not empty_only or not os.listdir(path))  # all dirs allowed or is empty
                ):
                    modification_age = (datetime.datetime.now()
                                        - datetime.datetime.fromtimestamp(st[ST_CTIME]))
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
    def disk_usage(path):
        """Return disk usage statistics about the given path.

        Returned values is a named tuple with attributes 'total', 'used' and
        'free', which are the amount of total, used and free space, in bytes.
        """
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        _n_tuple_disk_usage = namedtuple('usage', 'total used free')
        return _n_tuple_disk_usage(total, used, free)

    @staticmethod
    def get_emptiest_volume(
            volumes: List[Volume],
            logger=Logger(False)
    ) -> Volume:
        logger.log('%d possible target volumes. Searching for emptiest...' % len(volumes), 0, 1)
        volume_with_most_free_space = OsOperations.get_volume_with_most_extreme_free_space(
            volumes,
            lowest=False,
            logger=logger
        )
        logger.log('search for emptiest volume finished', -1)
        return volume_with_most_free_space

    @staticmethod
    def get_fullest_volume(
            volumes: List[Volume],
            logger=Logger(False)
    ) -> Volume:
        logger.log('%d possible target volumes. Searching for fullest...' % len(volumes), 0, 1)
        volume_with_most_free_space = OsOperations.get_volume_with_most_extreme_free_space(
            volumes,
            lowest=True,
            logger=logger
        )
        logger.log('search for fullest volume finished', -1)
        return volume_with_most_free_space

    @staticmethod
    def get_volume_with_most_extreme_free_space(
            volumes: List[Volume],
            lowest,
            logger=Logger(False)
    ) -> Volume:
        most_extreme_free_space_in_percent = -1
        volume_with_most_extreme_free_space = None
        for volume in volumes:
            volume_usage = OsOperations.disk_usage(volume.get_absolute_path())
            free_space_in_percent = (100 / volume_usage.total) * volume_usage.free
            logger.log('volume %s: %d%% empty' % (volume.to_string(), free_space_in_percent))
            if (
                    most_extreme_free_space_in_percent == -1
                    or (lowest and free_space_in_percent < most_extreme_free_space_in_percent)
                    or (not lowest and free_space_in_percent > most_extreme_free_space_in_percent)
            ):
                most_extreme_free_space_in_percent = free_space_in_percent
                volume_with_most_extreme_free_space = volume
        return volume_with_most_extreme_free_space

    @staticmethod
    def move(source, destination, stop_sonarr=False, create_symlinks_after=False, test_run=False, logger=Logger(False)):
        OsOperations.move_multiple([source], destination, stop_sonarr, create_symlinks_after, test_run, logger)

    @staticmethod
    def __move(source, destination, test_run=False, logger=Logger(False)):
        if test_run:
            logger.log('test run: move("%s", "%s")' % (source, destination))
        else:
            logger.log('move("%s", "%s")' % (source, destination))
            if not os.path.exists(destination):
                os.makedirs(destination)
            move(source, destination)

    @staticmethod
    def move_multiple(sources, destination, stop_sonarr=False, create_symlinks_after=False, test_run=False,
                      logger=Logger(False)):
        from space_manager_helpers import SonarrApi
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
            directories,
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
    def get_tree_size(path):
        """Return total size of files in given path and subdirs."""
        total = 0
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                total += OsOperations.get_tree_size(entry.path)
            else:
                total += entry.stat(follow_symlinks=False).st_size
        return total
