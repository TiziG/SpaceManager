import datetime

from space_manager.smlib.config import CATEGORY_COLLECTION, DistributerConfig
from space_manager.smlib.core.delete import FolderDeleter
from space_manager.smlib.core.distribute import Distributor
from space_manager.smlib.helpers import Logger


def delete_empty_folders(minimum_age, test_run, logging):
    logger = Logger(logging)
    logger.log("delete_empty_folders called", 0, 1, forced=True)
    folder_deleter = FolderDeleter(test_run, logger)
    for folder in CATEGORY_COLLECTION.all_folders:
        folder_deleter.delete_empty_folders(folder, minimum_age)
    logger.log("distribute_folders end", -1, forced=True)


def distribute_folders(minimum_age=datetime.timedelta(hours=5),
                       test_run=False,
                       logging=False):
    logger = Logger(logging)
    logger.log("distribute_folders called", 0, 1, forced=True)
    for category in CATEGORY_COLLECTION.categories:
        distributor = Distributor(
            category,
            DistributerConfig(
                minimum_age=minimum_age,
                test_run=test_run,
                logger=logger,
            )
        )
        distributor.distribute_from_link_folders()
    logger.log("distribute_folders end", -1, forced=True)


def redistribute_folders(nr_of_runs, fullest_threshold, minimum_age, test_run, logging):
    config = DistributerConfig(
        fullest_threshold=fullest_threshold,
        nr_of_runs=nr_of_runs,
        minimum_age=minimum_age,
        test_run=test_run,
        logger=Logger(logging)
    )
    config.logger.log("redistribute_folders called", 0, 1, forced=True)
    for i in range(config.nr_of_runs):
        config.logger.divider()
        config.logger.log("Run %d of %d" % (i + 1, config.nr_of_runs), 0, 1)
        for category in CATEGORY_COLLECTION.categories:
            distributer = Distributor(category, config)
            distributer.distribute_from_data_folders()
        config.logger.change_indentation(-1)
    config.logger.log("redistribute_folders end", -1, forced=True)
