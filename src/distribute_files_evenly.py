#!/usr/local/bin/python
#  distribute_files_evenly.py

from collections import namedtuple

from config import CategoryAndVolumeDefinitions
from distribute_files_evenly_core import Distributer
from space_manager_helpers import Logger

_n_tuple_config = namedtuple('config', 'fullest_threshold')

# configuration-----------
TEST_RUN = True
LOGGING = True
CONFIG = _n_tuple_config(0.75)
# ------------------------


if __name__ == '__main__':
    distributer = Distributer(config=CONFIG, test_run=TEST_RUN, logger=Logger(LOGGING))
    for category in CategoryAndVolumeDefinitions.categories.categories:
        distributer.distribute(category)
