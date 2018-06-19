import datetime

from space_manager.smlib import commands
from space_manager.smlib.config import CATEGORY_COLLECTION


def delete_empty_folders(
        minimum_age=1,
        test_run=False,
        logging=False):
    commands.delete_empty_folders(datetime.timedelta(hours=minimum_age), test_run, logging)


def distribute_folders(
        minimum_age=5,
        test_run=False,
        logging=False):
    commands.distribute_folders(datetime.timedelta(hours=minimum_age), test_run, logging)


def redistribute_folders(
        nr_of_runs=1,
        fullest_threshold=75,
        minimum_age=1,
        categories=CATEGORY_COLLECTION.keys,
        test_run=False,
        logging=False):
    commands.redistribute_folders(nr_of_runs, float(fullest_threshold) / float(100),
                                  datetime.timedelta(hours=minimum_age), categories, test_run, logging)
