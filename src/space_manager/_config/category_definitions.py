# category_and_volumes_definition

from .voleme_factory import volume_factory
from .._shared_objects import Category, CategoryCollection, DiskInfo

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
            DiskInfo(10, 1)
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
            DiskInfo(6, 4)
        ])
    )
])
