#  redistribute_folders.py

import datetime

from space_manager._config import CATEGORY_COLLECTION, DistributerConfig
from space_manager._distribute_core import Distributer
from space_manager._helpers import Logger

# configuration-----------
TEST_RUN = False
LOGGING = True
NR_OF_RUNS = 2
FULLEST_THRESHOLD = 0.75
MINIMUM_AGE = datetime.timedelta(hours=1)


# ------------------------


def redistribute_folders():
    config = DistributerConfig(
        nr_of_runs=NR_OF_RUNS,
        fullest_threshold=FULLEST_THRESHOLD,
        minimum_age=MINIMUM_AGE,
        test_run=TEST_RUN,
        logger=Logger(LOGGING)
    )
    for i in range(config.nr_of_runs):
        config.logger.divider()
        config.logger.log("Run %d of %d" % (i + 1, config.nr_of_runs), 0, 1)
        for category in CATEGORY_COLLECTION.categories:
            distributer = Distributer(category, config)
            distributer.distribute_from_data_folders()
        config.logger.change_indentation(-1)
