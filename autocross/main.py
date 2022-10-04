"""Main entry point for autocross

"""

# Standard library imports
import sys

# Local application imports
import analyze
import calculate
import cli
import plot
import schedule
from cmd_dispatch import CmdDispatcher


# pylint: disable=E1136  # Suppress unsubscriptable error for type hints
def _main(argv: list[str]) -> int:
    """Main entrypoint into crossroads

    :param argv: commandline arguments
    :return: 0 for normal exist, non-zero otherwise
    """
    dispatcher = CmdDispatcher()
    dispatcher.register_command('analyze', analyze.analyze_main)
    dispatcher.register_command('calculate', calculate.calculate_main)
    dispatcher.register_command('plot', plot.plot_main)
    dispatcher.register_command('schedule', schedule.schedule_main)

    args = cli.parse_args(argv)
    dispatcher.dispatch(args.command, args)

    return 0


if __name__ == '__main__':
    # argv[0] is the program name, so we don't need it
    sys.exit(_main(sys.argv[1:]))
