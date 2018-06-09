#!/usr/local/bin/python
#  distribute_files_evenly.py

import datetime

from space_manager.config import CategoryAndVolumeDefinitions, DistributerConfig
from space_manager.distribute_core import Distributer
from space_manager.helpers import Logger

# configuration-----------
TEST_RUN = False
LOGGING = True
NR_OF_RUNS = 2
FULLEST_THRESHOLD = 0.75
MINIMUM_AGE = datetime.timedelta(hours=1)
# ------------------------


if __name__ == '__main__':
    CONFIG = DistributerConfig(
        nr_of_runs=NR_OF_RUNS,
        fullest_threshold=FULLEST_THRESHOLD,
        minimum_age=MINIMUM_AGE,
        test_run=TEST_RUN,
        logger=Logger(LOGGING)
    )
    for i in range(CONFIG.nr_of_runs):
        CONFIG.logger.divider()
        CONFIG.logger.log("Run %d of %d" % (i + 1, CONFIG.nr_of_runs), 0, 1)
        for category in CategoryAndVolumeDefinitions.categories.categories:
            distributer = Distributer(category, CONFIG)
            distributer.distribute_from_data_folders()
        CONFIG.logger.change_indentation(-1)
