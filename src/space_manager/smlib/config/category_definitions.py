# category_and_volumes_definition

from space_manager.smlib.models import Category, CategoryCollection, DiskInfo
from .volume_factory import volume_factory

CATEGORY_COLLECTION = CategoryCollection([
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
            DiskInfo(10, 1),
            # DiskInfo(10, 2)
        ])
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
            DiskInfo(6, 4),
            DiskInfo(10, 1),
            # DiskInfo(10, 2)
        ])
    )
])
