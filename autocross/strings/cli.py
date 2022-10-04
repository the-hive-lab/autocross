"""Strings file for the autocross.cli module

This module contains string definitions for the autocross.cli module
"""

from typing import Final

# Main parser strings
PROGRAM_NAME: Final[str] = 'autocross'
PROGRAM_DESCRIPTION: Final[str] = f'{PROGRAM_NAME} is a tool for scheduling ' \
                                  'and analyzing intersection crossings for ' \
                                  'autonomous vehicles.'

# Sub parser strings
SUBPARSERS_TITLE: Final[str] = f'{PROGRAM_NAME} commands'
SUBPARSERS_DEST: Final[str] = 'command'

# Calculate subcommand strings
CALC_PARSER_NAME: Final[str] = 'calculate'
CALC_PARSER_HELP: Final[str] = "generate a vehicle's crossing cost file"
CALC_ARG_VEHICLE_FILE: Final[str] = 'vehicle_file'
CALC_ARG_TIME_MIN: Final[str] = 'time_min'
CALC_ARG_TIME_MAX: Final[str] = 'time_max'
CALC_ARG_TIME_STEP: Final[str] = 'time_step'
CALC_ARG_DIRECTION: Final[str] = '--direction'

# Schedule subcommand strings
SCHED_PARSER_NAME: Final[str] = 'schedule'
SCHED_PARSER_HELP: Final[str] = 'generate a crossing schedule'
SCHED_ARG_COST_FILES: Final[str] = 'cost_files'
SCHED_ARG_OUTPUT_FILE: Final[str] = '--output_file'
SCHED_ARG_CROSS_SUM: Final[str] = '--cross_sum'
SCHED_ARG_SCHED_TYPE: Final[str] = 'schedule_type'
SCHED_TYPE_FCF: Final[str] = 'fcf'
SCHED_TYPE_FCFS: Final[str] = 'fcfs'
SCHED_TYPE_RAND: Final[str] = 'rand'
SCHED_TYPE_FIXED: Final[str] = 'fixed'

# Analyze subcommand strings
ANALYZE_PARSER_NAME: Final[str] = 'analyze'
ANALYZE_PARSER_HELP: Final[str] = 'analyze a crossing schedule'
ANALYZE_ARG_SCHED_FILE: Final[str] = 'schedule_file'
ANALYZE_ARG_COST_FILEPATHS: Final[str] = '--cost_filepaths'
ANALYZE_ARG_WAIT_FILEPATHS: Final[str] = '--wait_filepaths'

# Plot subcommand strings
PLOT_PARSER_NAME: Final[str] = 'plot'
PLOT_PARSER_HELP: Final[str] = "plot a vehicle's cost or system file"
PLOT_ARG_FILEPATHS: Final[str] = 'filepaths'
PLOT_ARG_SCHED_FILE: Final[str] = '--schedule'
