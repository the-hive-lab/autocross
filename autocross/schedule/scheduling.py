import random
from typing import Optional


def scheduled_random(num_vehicles: int, seed: Optional = None) -> list:
    """Return a random crossing order

    Generates a list of crossing slots where element indices correspond
    to the vehicle IDs. Crossing order is randomly determined. For example,
    in the list [2, 1, 3], vehicle 0 would be in slot 1, vehicle 1 would be
    in slot 0, and vehicle 2 would be in slot 2. The returned list would
    look like [1, 0, 2].

    :param num_vehicles: number of vehicles
    :param seed: (optional) seed value for shuffler
    :return: list of crossing slots where element index corresponds
    to vehicle ID
    """
    random.seed(seed)
    vehicles = list(range(num_vehicles))
    random.shuffle(vehicles)

    return vehicles


def scheduled_first_come_first_serve(arrival_times: list) -> list:
    """Return a first-come-first-serve crossing order

    Generates a list of crossing slots where element indices correspond
    to vehicle IDs. Crossing order is in a non-decreasing order of vehicles'
    arrival times. For example, in the list [4, 3, 5], vehicle 0 would be
    in slot 1, vehicle 1 would be in slot 0, and vehicle 2 would be in slot 2.
    The returned list would look like [1, 0, 2].

    :param arrival_times: list of vehicle arrival times
    :return: list of crossing slots where element index corresponds
    to vehicle ID
    """
    return _scheduled_non_decreasing(arrival_times)


def scheduled_fastest_crossing_first(crossing_times: list) -> list:
    """Return a fastest-crossing-first crossing order

    Generates a list of crossing slots where element indices correspond
    to vehicle IDs. Crossing order is determined based on vehicles' crossing
    times. For example, in the list [6, 10, 23], vehicle 0 would be in slot 0,
    vehicle 1 would be in slot 1, and vehicle 2 would be in slot 2. The
    return list would look like [0, 1, 2].

    :param crossing_times: list of vehicle crossing times
    :return: list of crossing slots where element index corresponds
    to vehicle ID
    """
    return _scheduled_non_decreasing(crossing_times)


def scheduled_socially_aware():
    pass


def _scheduled_non_decreasing(values: list) -> list:
    """Return a non-decreasing schedule

    Generates a list of values where element indices correspond to indices
    of inputted list. Values are determined based on non-decreasing ordering
    of inputted list. For example, in the list [4, 6, 5], element 0 would be
    given value 0, element 1 would be given value 2, and element 2 would be
    given value 1. The returned list would look like [0, 2, 1].

    :param values: list of values to schedule
    :return: list of values with a value representing where in a sorted list
    it would be located.
    """
    tuples_list = [(value, index) for index, value in enumerate(values)]
    schedule = [-1] * len(values)

    # tuples_list is [(value, original index), (value, original index), ...]
    # When enumerating we get [(sort index, value, original index), ...]
    for sort_index, tup_elem in enumerate(sorted(tuples_list)):
        _, original_index = tup_elem
        schedule[original_index] = sort_index

    assert -1 not in schedule, 'At least one vehicle did not get scheduled'

    return schedule
