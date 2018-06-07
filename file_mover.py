# file_mover.py

import os
import re
import datetime
from collections import namedtuple
from stat import S_ISDIR, ST_CTIME
from typing import List
from shutil import move
from subprocess import call
from logger import Logger
from disk_info import DiskInfo


class FileMover(object):
    VOLUME_PREFIX = 'Data'
    MOUNT_POINT = r'/mnt/'
    MINIMUM_AGE = datetime.timedelta(hours=5)

    def __init__(self, test_run=False, logger=Logger(False)):
        self._test_run = test_run
        self._logger = logger

    def move_folders(self, folder_name_prefix, source_volumes, target_volumes):
        self._logger.divider()
        self._logger.log('start of main function for ' + folder_name_prefix, 0, 1)
        self._logger.log('test run is set to %s' % str(self._test_run))
        target_volume = self.__most_free_space(target_volumes)
        self._logger.log('target volume set to: ' + target_volume.to_string())
        self._logger.log('Search in %d source volume(s) for new folders' % len(source_volumes), 0, 1)
        source_folder_paths = self.__get_folder_paths_to_move(folder_name_prefix, source_volumes)
        self._logger.log('search for new folders finished. Found %d' % len(source_folder_paths), -1)
        if source_folder_paths:
            self.__stop_sonarr()
            for path in source_folder_paths:
                self.__actually_move(path, self.__folder_path(folder_name_prefix, target_volume, True))
            self.__create_symlinks()
        self._logger.log('end of main function', -1)
        self._logger.divider()

    def __actually_move(self, source, destination):
        if self._test_run:
            self._logger.log('test run: move("%s", "%s")' % (source, destination))
        else:
            self._logger.log('move("%s", "%s")' % (source, destination))
            move(source, destination)

    def __get_folder_paths_to_move(self, folder_name_prefix, source_volumes):
        folder_paths = []
        for source_volume in source_volumes:
            folder_paths.extend(
                self.__get_sub_folders(self.__folder_path(folder_name_prefix, source_volume))
            )
        return folder_paths

    @staticmethod
    def __folder_name(prefix: str, disk_info: DiskInfo, is_link_target=False) -> str:
        return prefix + disk_info.to_string(is_link_target)

    def __folder_path(self, folder_prefix: str, disk_info: DiskInfo, is_link_target=False) -> str:
        return (self.__volume_path(disk_info)
                + self.__folder_name(folder_prefix, disk_info, is_link_target)
                + '/')

    def __volume_path(self, disk_info: DiskInfo) -> str:
        return FileMover.MOUNT_POINT + self.__folder_name(FileMover.VOLUME_PREFIX, disk_info) + '/'

    def __stop_sonarr(self):
        if self._test_run:
            self._logger.log('test run: warden stop sonarr_2')
        else:
            self._logger.log('stopping sonarr...')
            call(["warden", "stop", "sonarr_2"])
            self._logger.log('...stopping sonarr done')

    def __create_symlinks(self):
        if self._test_run:
            self._logger.log('test run: sh /mnt/Data2TB-V1/Files2TB-V1/FreeNasScripts/createSymLinks.sh')
        else:
            self._logger.log('sh /mnt/Data2TB-V1/Files2TB-V1/FreeNasScripts/createSymLinks.sh')
            call(["sh", '/mnt/Data2TB-V1/Files2TB-V1/FreeNasScripts/createSymLinks.sh'])

    def __most_free_space(self, volumes: List[DiskInfo]) -> DiskInfo:
        most_free_space_in_percent = 0
        volume_with_most_free_space = None
        self._logger.log('%d possible target volumes. Searching for emptiest...' % len(volumes), 0, 1)
        for volume in volumes:
            volume_usage = self.__disk_usage(self.__volume_path(volume))
            free_space_in_percent = (100 / volume_usage.total) * volume_usage.free
            self._logger.log('volume %s: %d%% empty' % (volume.to_string(), free_space_in_percent))
            if free_space_in_percent > most_free_space_in_percent:
                most_free_space_in_percent = free_space_in_percent
                volume_with_most_free_space = volume
        self._logger.log('search for emptiest volume finished', -1)
        return volume_with_most_free_space

    @staticmethod
    def __get_data_volumes():
        volumes = []
        for volume in os.listdir('/mnt/'):
            if re.match(r'^Data\d+TB-V\d$', volume):
                volumes.append(volume)
        return volumes

    def __get_sub_folders(self, parent_path):
        sub_folders = []
        for filename in os.listdir(parent_path):
            path = os.path.join(parent_path, filename)
            try:
                st = os.lstat(path)  # get info about the file (don't follow symlinks)
            except EnvironmentError:
                continue  # file vanished or permission error
            else:
                if S_ISDIR(st.st_mode):  # is regular directory?
                    modification_age = (datetime.datetime.now()
                                        - datetime.datetime.fromtimestamp(st[ST_CTIME]))
                    if modification_age > FileMover.MINIMUM_AGE:
                        sub_folders.append(path)
                    else:
                        self._logger.log('Found a folder but its age (%dmin) is less than %dmin: %s'
                                         % (modification_age.seconds // 60,
                                            FileMover.MINIMUM_AGE.seconds // 60,
                                            filename))
        return sub_folders

    @staticmethod
    def __disk_usage(path):
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
