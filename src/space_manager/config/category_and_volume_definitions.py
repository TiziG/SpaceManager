# category_and_volumes_definition

from typing import List

from space_manager.shared_objects import Categories, Category, DiskInfo, Volume

DEFAULT_MOUNT_POINT = r'/mnt/'
DEFAULT_DATA_PREFIX = 'Data'


def volume_factory(disk_infos: List[DiskInfo],
                   mount_point=DEFAULT_MOUNT_POINT,
                   vol_prefix=DEFAULT_DATA_PREFIX) -> List[Volume]:
    volumes = []
    for disk_info in disk_infos:
        volumes.append(Volume(mount_point, vol_prefix, disk_info))
    return volumes


class CategoryAndVolumeDefinitions(object):
    categories = Categories([
        Category(
            prefix='Series',
            sonarr_related=True,
            link_source_volumes=volume_factory([
                DiskInfo(4, 1)
            ]),
            data_volumes=volume_factory([
                DiskInfo(4, 1),
                DiskInfo(4, 2),
                DiskInfo(4, 3),
                DiskInfo(4, 4),
                DiskInfo(10, 1)
            ])),
        Category(
            prefix='Movies',
            link_source_volumes=volume_factory([
                DiskInfo(6, 1)
            ]),
            data_volumes=volume_factory([
                DiskInfo(6, 1),
                DiskInfo(6, 2),
                DiskInfo(6, 3),
                DiskInfo(6, 4)
            ]))
    ])
