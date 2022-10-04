from typing import Final, Sequence

import casadi


EPSILON: Final = 0.00001


def assign_optimal_crossing_times(cost_funcs: Sequence,
                                  cost_bounds: Sequence,
                                  **kwargs) -> list:
    """Assigns crossing times to each vehicle

    Crossing times are assigned such that they maximize passengers'
    overall preferences. Each vehicle's passengers' preferences are
    represented by a cost function. The `costs_bounds` variable
    specifies the range in which a vehicle's crossing cost function
    is defined. The lower bound is typically determined by a vehicle's
    dynamics limitations, meaning it physically cannot cross the
    intersection in the specified amount of time.

    :param cost_funcs: list of vehicles' crossing functions. Cost
    functions must be CasADi `interpolant` objects.
    :param cost_bounds: list of vehicle' crossing function bounds. List
    elements should be tuples formatted as `[(lower, upper), ...]`
    :return: list of vehicles' assigned crossing times. The vehicle
    ordering is preserved.
    """
    assert(len(cost_funcs) == len(cost_bounds))

    opti = casadi.Opti()

    time_vars = [opti.variable() for _ in cost_funcs]
    time_costs = [func(time) for func, time in zip(cost_funcs, time_vars)]

    slack_var = opti.variable()

    # opti.minimize(sum(time_costs))
    opti.minimize(sum(time_costs) + 100 * slack_var)

    for time, bounds in zip(time_vars, cost_bounds):
        lower = bounds[0] + EPSILON
        upper = bounds[1] - EPSILON
        opti.subject_to(opti.bounded(lower, time, upper))

    if 'cross_sum' in kwargs:
        # opti.subject_to(sum(time_vars) <= kwargs['cross_sum'])
        opti.subject_to(sum(time_vars) <= kwargs['cross_sum'] + slack_var)
        opti.subject_to(slack_var >= 0)

    try:
        opti.solver('ipopt')
        solution = opti.solve()
    except RuntimeError:
        raise ValueError('Cannot assign crossing times with given cost '
                         'functions and bounds')

    return [solution.value(time_var) for time_var in time_vars]
