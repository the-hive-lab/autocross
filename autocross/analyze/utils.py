def start_times_from_schedule(crossing_order: list,
                              crossing_times: list) -> list:
    """Generate a list of starting times from crossing schedule

    Each start time is the previous vehicle's start time plus the
    previous vehicle's crossing time. Start times determine when a
    vehicle can cross the intersection.

    :param crossing_order: list of crossing slots where vehicle ID is
    based on its position in the list
    :param crossing_times: list of crossing times where vehicle ID is
    based on its position in the list
    :return: list of start times for each vehicle
    """
    assert len(crossing_order) == len(crossing_times)

    triple_list = [(slot, vid, time)
                   for vid, (slot, time)
                   in enumerate(zip(crossing_order, crossing_times))]

    triple_list.sort()

    start = 0
    start_times = [-1] * len(crossing_order)

    for _, vid, time in triple_list:
        start_times[vid] = start
        start += time

    assert -1 not in start_times, "At least one vehicle without start time"

    return start_times
