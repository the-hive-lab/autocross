def sum_waiting_costs(cost_funcs: list, start_times: list) -> float:
    """Sum all of the waiting costs

    A vehicle's waiting cost is a function of its start time, which is
    the time at which they are permitted to cross the intersection.

    :param cost_funcs: list of waiting cost functions
    :param start_times: list of start times where the first vehicle to
    cross has a start time of 0
    :return: sum of waiting costs among all vehicles
    """
    return _sum_costs(cost_funcs, start_times)


def sum_crossing_costs(cost_funcs: list, crossing_times: list) -> float:
    """Sum all of the crossing costs

    A vehicle's crossing cost is a function of its assigned crossing
    time. Given vehicle crossing cost functions and their assigned
    times, the total cost for all vehicles can be calculated. Vehicles
    are determined base on their position in the lists. For example,
    Vehicle 0 is the 0th element in both lists. It is assumed that both
    lists have the same ordering.

    :param cost_funcs: list of crossing cost functions
    :param crossing_times: list of assigned crossing times
    :return: total crossing cost among all vehicles
    """
    return _sum_costs(cost_funcs, crossing_times)


def _sum_costs(cost_funcs: list, func_inputs: list) -> float:
    """Sum output of all functions

    Given a list of functions and a list of function inputs, sum the
    outputs of all functions in the given list. Functions are evaluated
    element-wise, and it is assumed that both lists have the same
    ordering. For example, the lists are evaluated func_0(input_0),
    func_1(input_1), ...

    :param cost_funcs: list of cost functions
    :param func_inputs: list of function inputs
    :return: sum of all function outputs
    """
    assert len(cost_funcs) == len(func_inputs)

    return sum([func(input_) for func, input_ in zip(cost_funcs, func_inputs)])


def calc_intersection_clearing_time(crossing_times: list) -> float:
    """Calculate total time needed to clear intersection

    Clearing intersection means all vehicles currently stopped and
    ready to go through the intersection have gone through. In other
    words, all vehicles that are first in line for their lane.

    :param crossing_times: list of crossing times (how long each
    vehicle has to cross the intersection)
    :return: total time needed for all lead vehicles to cross
    """
    return sum(crossing_times)