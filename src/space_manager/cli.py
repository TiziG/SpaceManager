import argparse
from enum import Enum

from space_manager import api
from space_manager.smlib.config import CATEGORY_COLLECTION


class Options(Enum):
    LOGGING = 'logging'
    TEST_RUN = 'test_run'
    MINIMUM_AGE = 'minimum_age'
    FULLEST_THRESHOLD = 'fullest_threshold'
    CATEGORIES = 'categories'


def parse_arguments(args):
    return {option.value: getattr(args, option.value) for option in Options
            if hasattr(args, option.value) and getattr(args, option.value) is not None}


def delete_empty_folders(args):
    api.delete_empty_folders(**parse_arguments(args))


def distribute_folders(args):
    api.distribute_folders(**parse_arguments(args))


def redistribute_folders(args):
    api.redistribute_folders(**parse_arguments(args))


def run() -> None:
    parser = argparse.ArgumentParser(description="performs various file system tasks, specific to NAS2")
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # global options
    parser.add_argument("-v", "--verbose", dest=Options.LOGGING.value, action="store_true", help="verbose logging")
    parser.add_argument("-t", "--test-run", dest=Options.TEST_RUN.value, action="store_true",
                        help="runs without changing any files")

    # command delete-empty-folders
    parser_delete_empty_folders = subparsers.add_parser(
        'delete-empty', help='deletes all empty folders in all Dx and Vx directories')
    parser_delete_empty_folders.add_argument(
        "-a", "--minimum-age", dest=Options.MINIMUM_AGE.value, type=int,
        help="minimum age in hours for empty folders to be deleted")
    parser_delete_empty_folders.set_defaults(func=delete_empty_folders)

    # command distribute-new-folders
    parser_distribute_folders = subparsers.add_parser(
        'distribute',
        help='moves all folders (no links) from Vx directories to the Dx directory with the most free space. '
             + 'It then creates symlinks')  # pylint: disable=bad-continuation
    parser_distribute_folders.add_argument("-a", "--minimum-age", dest=Options.MINIMUM_AGE.value,
                                           help="minimum age in hours for folders to be moved", type=int)
    parser_distribute_folders.set_defaults(func=distribute_folders)

    # command redistribute-folders-evenly
    parser_redistribute_folders = subparsers.add_parser(
        'redistribute', help='moves folders from one Dx directory to another one with more free space')
    parser_redistribute_folders.add_argument(
        "-a", "--minimum-age", dest=Options.MINIMUM_AGE.value, type=int,
        help="minimum age in hours for folders to be moved")
    parser_redistribute_folders.add_argument(
        "-f", "--fullest-threshold", dest=Options.FULLEST_THRESHOLD.value, type=int, choices=range(100),
        help="minimum used space in %% of the fullest volume to start redistribution")
    parser_redistribute_folders.add_argument(
        "-c", "--categories", dest=Options.CATEGORIES.value, type=str, nargs='+', choices=CATEGORY_COLLECTION.keys,
        help="limit redistribution to specific categories")
    parser_redistribute_folders.set_defaults(func=redistribute_folders)

    args = parser.parse_args()
    args.func(args)
