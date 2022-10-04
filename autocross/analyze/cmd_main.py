# Local application imports
from autocross import fileio
from autocross.analyze import metrics
from autocross.analyze import utils


def analyze_main(args):
    schedule_data = fileio.read_schedule_file(args.schedule_file)
    crossing_order, crossing_times = fileio.parse_schedule_data(schedule_data)

    cross_cost_funcs = []
    wait_cost_funcs = []

    for cost_filepath in args.cost_filepaths:
        cost_data = fileio.read_cost_file(cost_filepath)
        cross_cost_func, _ = fileio.parse_cost_data(cost_data)

        cross_cost_funcs.append(cross_cost_func)

    for wait_filepath in args.wait_filepaths:
        wait_data = fileio.read_cost_file(wait_filepath)
        wait_cost_func, _ = fileio.parse_cost_data(wait_data)

        wait_cost_funcs.append(wait_cost_func)

    start_times = utils.start_times_from_schedule(crossing_order,
                                                  crossing_times)

    wait_cost = metrics.sum_waiting_costs(wait_cost_funcs, start_times)
    cross_cost = metrics.sum_crossing_costs(cross_cost_funcs, crossing_times)
    clearing_time = metrics.calc_intersection_clearing_time(crossing_times)
    schedule_cost = wait_cost + cross_cost

    print(f'Schedule cost: {schedule_cost}')
    print(f'Clearing time: {clearing_time}')

    return 0
