import argparse

from space_manager import api
from space_manager.smlib.config import CATEGORY_COLLECTION

OPTIONS = [
    'logging',
    'test_run',
    'minimum_age',
    'fullest_threshold',
    'category'
]


def parse_arguments(args):
    return {option: getattr(args, option) for option in OPTIONS
            if hasattr(args, option) and getattr(args, option) is not None}


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
    parser.add_argument("-v", "--verbose", dest='logging', action="store_true", help="verbose logging")
    parser.add_argument("-t", "--test-run", dest='test_run', action="store_true",
                        help="runs without changing any files")

    # command delete-empty-folders
    parser_delete_empty_folders = subparsers.add_parser(
        'delete-empty', help='deletes all empty folders in all Dx and Vx directories')
    parser_delete_empty_folders.add_argument(
        "-a", "--minimum-age", dest='minimum_age', type=int,
        help="minimum age in hours for empty folders to be deleted")
    parser_delete_empty_folders.set_defaults(func=delete_empty_folders)

    # command distribute-new-folders
    parser_distribute_folders = subparsers.add_parser(
        'distribute',
        help='moves all folders (no links) from Vx directories to the Dx directory with the most free space. '
             + 'It then creates symlinks')  # pylint: disable=bad-continuation
    parser_distribute_folders.add_argument("-a", "--minimum-age", dest='minimum_age',
                                           help="minimum age in hours for folders to be moved", type=int)
    parser_distribute_folders.set_defaults(func=distribute_folders)

    # command redistribute-folders-evenly
    parser_redistribute_folders = subparsers.add_parser(
        'redistribute', help='moves folders from one Dx directory to another one with more free space')
    parser_redistribute_folders.add_argument(
        "-a", "--minimum-age", dest='minimum_age', type=int, help="minimum age in hours for folders to be moved")
    parser_redistribute_folders.add_argument(
        "-f", "--fullest-threshold", dest='fullest_threshold', type=int, choices=range(100),
        help="minimum used space in %% of the fullest volume to start redistribution")
    parser_redistribute_folders.add_argument(
        "-c", "--category", dest='category', type=str, choices=CATEGORY_COLLECTION.keys,
        help="limit redistribution to a category")
    parser_redistribute_folders.set_defaults(func=redistribute_folders)

    args = parser.parse_args()
    args.func(args)
