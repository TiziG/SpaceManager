from space_manager._helpers import Converter, Usage


class Check(object):
    @staticmethod
    def fullest_threshold_met(config, fullest_usage: Usage) -> bool:
        fullest_used = fullest_usage.used / fullest_usage.total
        config.logger.log("The Fullest disk is at %d%%. Threshold is %d%%" % (
            fullest_used * 100, config.fullest_threshold * 100))
        threshold_met = fullest_used > config.fullest_threshold
        config.logger.log_condition(threshold_met)
        return threshold_met

    @staticmethod
    def enough_free_space(config, emptiest_free: int, fullest_free: int) -> bool:
        minimum_free_needed = fullest_free * 2
        config.logger.log("Free space needed to start algorithm: %dGB" % (
            Converter.b_to_gb(minimum_free_needed)))
        config.logger.log("actual free space: %dGB" % (
            Converter.b_to_gb(emptiest_free)))
        enough_space = emptiest_free > minimum_free_needed
        config.logger.log_condition(enough_space)
        return enough_space
