#!/usr/local/bin/python
#  distribute_files_evenly.py

from collections import namedtuple

from space_manager.config import CategoryAndVolumeDefinitions
from space_manager.distribute_core import ReDistributer
from space_manager.helpers import Logger

Config = namedtuple('config', 'fullest_threshold nr_of_runs')

# configuration-----------
TEST_RUN = False
LOGGING = True
CONFIG = Config(0.75, 1)
# ------------------------


if __name__ == '__main__':
    for _ in range(CONFIG.nr_of_runs):
        distributer = ReDistributer(config=CONFIG, test_run=TEST_RUN, logger=Logger(LOGGING))
        for category in CategoryAndVolumeDefinitions.categories.categories:
            distributer.distribute_from_data_folders(category)
