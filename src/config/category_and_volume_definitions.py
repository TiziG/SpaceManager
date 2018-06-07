# category_and_volumes_definition

from shared_objects import DiskInfo, Category, Categories, Volume

DEFAULT_MOUNT_POINT = r'/mnt/'
DEFAULT_DATA_PREFIX = 'Data'


def volume_factory(disk_infos, mount_point=DEFAULT_MOUNT_POINT, vol_prefix=DEFAULT_DATA_PREFIX):
    volumes = []
    for disk_info in disk_infos:
        volumes.append(Volume(mount_point, vol_prefix, disk_info))
    return volumes


class CategoryAndVolumeDefinitions(object):
    categories = Categories([
        Category(
            prefix='Series',
            link_source_volumes=volume_factory([
                DiskInfo(4, 1)
            ]),
            data_volumes=volume_factory([
                DiskInfo(4, 1),
                DiskInfo(4, 2),
                DiskInfo(4, 3),
                DiskInfo(4, 4),
                DiskInfo(10, 1)
            ]),
        ),
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
            ])
        )
    ])
