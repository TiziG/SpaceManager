# sonarr_api.py

from subprocess import call

from .logger import Logger


class SonarrApi(object):

    @staticmethod
    def stop_sonarr(test_run=False, logger=Logger(False)):
        if test_run:
            logger.log('test run: warden stop sonarr_2')
        else:
            logger.log('stopping sonarr...')
            call(["warden", "stop", "sonarr_2"])
            logger.line()
            logger.log('...stopping sonarr done')

    @staticmethod
    def start_sonarr(test_run=False, logger=Logger(False)):
        if test_run:
            logger.log('test run: warden start sonarr_2')
        else:
            logger.log('starting sonarr...')
            call(["warden", "start", "sonarr_2"])
            logger.log('...starting sonarr done')
