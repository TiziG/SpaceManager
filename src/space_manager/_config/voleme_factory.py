from typing import List

from .mount_point_and_volume_config import DEFAULT_DATA_PREFIX, DEFAULT_MOUNT_POINT
from .._shared_objects import DiskInfo, Volume


def volume_factory(
        disk_infos: List[DiskInfo],
        mount_point=DEFAULT_MOUNT_POINT,
        vol_prefix=DEFAULT_DATA_PREFIX
) -> List[Volume]:
    return [Volume(mount_point, vol_prefix, disk_info) for disk_info in disk_infos]
