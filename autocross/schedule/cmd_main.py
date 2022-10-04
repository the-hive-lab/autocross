# Standard library imports
import argparse
import random

# Local application imports
import numpy as np

from autocross import fileio
from autocross.schedule import scheduling
from autocross.schedule import times


def schedule_main(args: argparse.Namespace) -> int:
    cost_files = args.cost_files
    cost_funcs = []
    cost_bounds = []

    for cost_file in cost_files:
        cost_data = fileio.read_cost_file(cost_file)
        cost_func, cost_bound = fileio.parse_cost_data(cost_data)
        cost_funcs.append(cost_func)
        cost_bounds.append(cost_bound)

    cross_times = []
    cross_order = []
    cross_costs = []

    if args.schedule_type == 'rand':
        pass
    if args.schedule_type == 'fcfs':
        cross_times = []

        for cost_func, cost_bound in zip(cost_funcs, cost_bounds):
            cross_times += \
                times.assign_optimal_crossing_times([cost_func], [cost_bound])

        arrival_times = list(range(len(args.cost_files)))
        random.shuffle(arrival_times)
        cross_order = scheduling.scheduled_first_come_first_serve(
            arrival_times)
    elif args.schedule_type == 'fcf':
        kwargs = dict()

        if args.cross_sum is not None:
            kwargs['cross_sum'] = args.cross_sum

        cross_times = times.assign_optimal_crossing_times(cost_funcs,
                                                          cost_bounds,
                                                          **kwargs)
        cross_order = scheduling.scheduled_fastest_crossing_first(cross_times)

        cross_costs = [float(func(time)) for func, time in zip(cost_funcs, cross_times)]

        schedule_data = [[time, cost] for time, cost in zip(cross_times, cross_costs)]
        np.savetxt(f'{args.output_file}.txt', schedule_data, header='time cost', comments='')
    elif args.schedule_type == 'fixed':
        cross_times = times.assign_optimal_crossing_times(cost_funcs,
                                                          cost_bounds)
        cross_order = list(range(len(args.cost_files)))

    file_dir = fileio.get_file_directory(cost_files[0])

    if args.output_file:
        output_file = args.output_file
    else:
        output_file = f'schedule.{args.schedule_type}'

    fileio.write_schedule_file(f'{file_dir}/{output_file}', cross_order,
                               cross_times)

    print(f'crossing times: {cross_times}')
    print(f'crossing costs: {cross_costs}')
    print(f'crossing order: {cross_order}')

    return 0
