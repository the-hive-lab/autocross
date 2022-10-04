# Standard library imports
import argparse

# Third party imports
import sys

import numpy as np

# Local application imports
from autocross import fileio
from autocross.calculate import costs
from autocross.calculate import vehicle
from autocross.calculate import reference


def calculate_main(args: argparse.Namespace) -> int:
    vehicle_data = fileio.read_vehicle_file(args.vehicle_file)
    veh = vehicle.build_vehicle(vehicle_data)

    times = np.arange(args.time_min, args.time_max + 1, args.time_step)

    results = dict()
    for time in times:
        delta_t = 0.1
        num_samples = costs.get_horizon(time, delta_t=delta_t)

        if args.direction == 'left':
            ref = reference.left_turn(num_samples + 1, 10)

            shifted_x = ref[0] + veh.state_bounds.initial[0]
            shifted_y = ref[1] + veh.state_bounds.initial[1]
            shifted_ref = np.stack((shifted_x, shifted_y))

            return_data = costs.calculate_with_reference(veh, time,
                                                         num_samples, delta_t,
                                                         shifted_ref)
        elif args.direction == 'right':
            ref = reference.right_turn(num_samples + 1, 5)

            shifted_x = ref[0] + veh.state_bounds.initial[0]
            shifted_y = ref[1] + veh.state_bounds.initial[1]
            shifted_ref = np.stack((shifted_x, shifted_y))

            return_data = costs.calculate_with_reference(veh, time,
                                                         num_samples, delta_t,
                                                         shifted_ref)
        else:
            # ref = None
            # return_data = costs.calculate(veh, time, num_samples, delta_t)
            ref = reference.straight_turn(num_samples + 1, 10)

            shifted_x = ref[0] + veh.state_bounds.initial[0]
            shifted_y = ref[1] + veh.state_bounds.initial[1]
            shifted_ref = np.stack((shifted_x, shifted_y))

            return_data = costs.calculate_with_reference(veh, time,
                                                         num_samples, delta_t,
                                                         shifted_ref)

        if return_data is not None:
            cost, states, inputs = return_data
            results[time] = {
                'cost': cost,
                'states': states,
                'inputs': inputs,
                'ref': ref,
            }
        else:
            results[time] = {'cost': None}
            print(f'No solution for time: {time}', file=sys.stderr)

    cost_list = [results['cost'] for results in results.values()]
    cost_func, cost_bounds = costs.costs_list_to_spline(times, cost_list)

    wait_factor = vehicle_data['wait_factor']
    wait_times = [time for time in np.arange(cost_bounds[0], cost_bounds[1])]
    wait_costs = [wait_factor * time for time in wait_times]
    wait_func, wait_bounds = costs.wait_costs_to_spline(wait_times, wait_costs)

    file_name = fileio.get_file_name(args.vehicle_file)
    file_dir = fileio.get_file_directory(args.vehicle_file)
    fileio.write_cost_file(f'{file_dir}/{file_name}.cost',
                           cost_func, cost_bounds)

    fileio.write_cost_file(f'{file_dir}/{file_name}.wait',
                           wait_func, wait_bounds)

    try:
        import matplotlib.pyplot as plt
        from math import sin, cos
        plt.quiver(results[8]['states'][0, :], results[8]['states'][1, :],
                   [cos(t) for t in results[8]['states'][2, :]],
                   [sin(t) for t in results[8]['states'][2, :]])
        plt.show()
        fileio.write_system_file(f'{file_dir}/{file_name}_08.system',
                                 results[8]['states'], results[8]['inputs'],
                                 ref=results[8]['ref'])
    except KeyError:
        pass
    try:
        fileio.write_system_file(f'{file_dir}/{file_name}_10.system',
                                 results[10]['states'], results[10]['inputs'],
                                 ref=results[8]['ref'])
    except KeyError:
        pass
    try:
        fileio.write_system_file(f'{file_dir}/{file_name}_15.system',
                                 results[15]['states'], results[15]['inputs'],
                                 ref=results[8]['ref'])
    except KeyError:
        pass

    return 0
