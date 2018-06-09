# distributer_config.py

import datetime
from collections import namedtuple

from .._helpers import Logger

# default _config ------------------------
FULLEST_THRESHOLD = 0.80
NR_OF_RUNS = 1
MINIMUM_AGE = datetime.timedelta(hours=0)
TEST_RUN = False
LOGGER = Logger(False)
# ---------------------------------------

DistributerConfig = namedtuple('DistributerConfig',
                               'fullest_threshold nr_of_runs minimum_age test_run logger')
DistributerConfig.__new__.__defaults__ = (
    FULLEST_THRESHOLD,
    NR_OF_RUNS,
    MINIMUM_AGE,
    TEST_RUN,
    LOGGER
)
