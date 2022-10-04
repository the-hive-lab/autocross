"""Command line argument parsing

This module contains the parsers for the main autocross command as well
as the subcommands.
"""

# Standard library imports
import argparse

# Local application imports
import strings.cli as res


_parser = argparse.ArgumentParser(prog=res.PROGRAM_NAME,
                                  description=res.PROGRAM_DESCRIPTION)
_subparsers = _parser.add_subparsers(title=res.SUBPARSERS_TITLE,
                                     dest=res.SUBPARSERS_DEST,
                                     required=True)

_calculate_parser = _subparsers.add_parser(res.CALC_PARSER_NAME,
                                           help=res.CALC_PARSER_HELP)
_calculate_parser.add_argument(res.CALC_ARG_VEHICLE_FILE, type=str)
_calculate_parser.add_argument(res.CALC_ARG_TIME_MIN, type=float)
_calculate_parser.add_argument(res.CALC_ARG_TIME_MAX, type=float)
_calculate_parser.add_argument(res.CALC_ARG_TIME_STEP, type=float)
_calculate_parser.add_argument(res.CALC_ARG_DIRECTION, type=str)

_schedule_parser = _subparsers.add_parser(res.SCHED_PARSER_NAME,
                                          help=res.SCHED_PARSER_HELP)
_schedule_parser.add_argument(res.SCHED_ARG_SCHED_TYPE, type=str,
                              choices=[res.SCHED_TYPE_FCF,
                                       res.SCHED_TYPE_FCFS,
                                       res.SCHED_TYPE_RAND,
                                       res.SCHED_TYPE_FIXED])
_schedule_parser.add_argument(res.SCHED_ARG_COST_FILES, type=str, nargs='*')
_schedule_parser.add_argument(res.SCHED_ARG_OUTPUT_FILE, type=str)
_schedule_parser.add_argument(res.SCHED_ARG_CROSS_SUM, type=float)

_analyze_parser = _subparsers.add_parser(res.ANALYZE_PARSER_NAME,
                                         help=res.ANALYZE_PARSER_HELP)
_analyze_parser.add_argument(res.ANALYZE_ARG_SCHED_FILE, type=str)
_analyze_parser.add_argument(res.ANALYZE_ARG_COST_FILEPATHS, type=str,
                             nargs='*')
_analyze_parser.add_argument(res.ANALYZE_ARG_WAIT_FILEPATHS, type=str,
                             nargs='*')

_plot_parser = _subparsers.add_parser(res.PLOT_PARSER_NAME,
                                      help=res.PLOT_PARSER_HELP)
_plot_parser.add_argument(res.PLOT_ARG_FILEPATHS, type=str, nargs='*')
_plot_parser.add_argument(res.PLOT_ARG_SCHED_FILE, type=str)


# pylint: disable=E1136  # Suppress unsubscriptable error for type hints
def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse commandline arguments

    :param argv: list of commandline arguments
    :return: Namespace containing the parsed results
    """
    return _parser.parse_args(argv)
