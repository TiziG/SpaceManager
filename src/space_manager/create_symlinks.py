# create_sym_links.py
from subprocess import call

from space_manager.helpers import Logger


def create_symlinks(test_run=False, logger=Logger(False)):
    if test_run:
        logger.log('test run: sh /mnt/Data2TB-V1/Files2TB-V1/FreeNasScripts/createSymLinks.sh')
    else:
        logger.log('calling createSymLinks.sh...')
        call(["sh", '/mnt/Data2TB-V1/Files2TB-V1/FreeNasScripts/createSymLinks.sh'])
        logger.log('...createSymLinks.sh done')


if __name__ == '__main__':
    create_symlinks()
