#!/usr/local/bin/python
#  distribute_folders.py

import datetime

from space_manager._config import CATEGORY_COLLECTION, DistributerConfig
from space_manager._distribute_core import Distributer
from space_manager._helpers import Logger

# configuration-----------
TEST_RUN = False
LOGGING = True
MINIMUM_AGE = datetime.timedelta(hours=5)


# ------------------------

def distribute_folders():
    for category in CATEGORY_COLLECTION.categories:
        distributor = Distributer(
            category,
            DistributerConfig(
                test_run=TEST_RUN,
                logger=Logger(LOGGING),
                minimum_age=MINIMUM_AGE
            )
        )
        distributor.distribute_from_link_folders()
