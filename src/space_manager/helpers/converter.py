class Converter(object):
    @staticmethod
    def b_to_gb(b: int) -> int:  # pylint: disable=invalid-name
        return int(b / 1_000_000_000)
