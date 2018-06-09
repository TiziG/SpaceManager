# sonarr.py

from subprocess import call

from space_manager.smlib.helpers.logger import Logger


class Sonarr(object):

    @staticmethod
    def stop(test_run=False, logger=Logger(False)):
        if test_run:
            logger.log('test run: warden stop sonarr_2')
        else:
            logger.log('stopping sonarr...')
            call(["warden", "stop", "sonarr_2"])
            logger.line()
            logger.log('...stopping sonarr done')

    @staticmethod
    def start(test_run=False, logger=Logger(False)):
        if test_run:
            logger.log('test run: warden start sonarr_2')
        else:
            logger.log('starting sonarr...')
            call(["warden", "start", "sonarr_2"])
            logger.log('...starting sonarr done')
