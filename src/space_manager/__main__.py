"""Space Manager command line tool."""

from space_manager.cli import run


def console_entry() -> None:
    run()


if __name__ == '__main__':
    run()
