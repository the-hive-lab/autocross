# Standard library imports
import math

# Third party imports
import casadi


def calculate(vehicle, crossing_time, num_samples, delta_t):
    """Calculate the cost for a vehicle to cross in given time

    This function solves a nonlinear optimization problem to determine
    the cost associated with the given vehicle crossing the
    intersection in the specified amount of time.

    :param vehicle: vehicle object that will be crossing
    :param crossing_time: time vehicle has to cross the intersection
    :param num_samples: number of samples in control horizon
    :param delta_t: time delta between samples
    :return:
    """
    opti = casadi.Opti()

    states = opti.variable(vehicle.num_states, num_samples + 1)
    inputs = opti.variable(vehicle.num_inputs, num_samples)

    cost = set_objective(opti, vehicle, states, inputs, crossing_time)

    discretize(opti, vehicle, states, inputs, num_samples, delta_t)

    set_bounds(opti, states, vehicle.state_bounds)
    set_bounds(opti, inputs, vehicle.input_bounds)

    options = {
        'ipopt.print_level': 0,  # Minimal printing
        'ipopt.sb': 'yes'  # Silence banner header
    }

    opti.solver('ipopt', options)
    try:
        solution = opti.solve()
        return (solution.value(cost), solution.value(states),
                solution.value(inputs))
    except RuntimeError:
        return None


def calculate_with_reference(vehicle, crossing_time, num_samples, delta_t,
                             ref):
    """Calculate the cost for a vehicle to cross in given time

    This function solves a nonlinear optimization problem to determine
    the cost associated with the given vehicle crossing the
    intersection in the specified amount of time.

    :param vehicle: vehicle object that will be crossing
    :param crossing_time: time vehicle has to cross the intersection
    :param num_samples: number of samples in control horizon
    :param delta_t: time delta between samples
    :param ref: reference trajectory to track
    :return:
    """
    opti = casadi.Opti()

    states = opti.variable(vehicle.num_states, num_samples + 1)
    inputs = opti.variable(vehicle.num_inputs, num_samples)

    cost = set_objective_with_ref(opti, vehicle, states, inputs, crossing_time,
                                  ref)

    # discretize(opti, vehicle, states, inputs, num_samples, delta_t)
    discretize_rk4(opti, vehicle, states, inputs, num_samples, delta_t)

    set_bounds(opti, states, vehicle.state_bounds)
    set_bounds(opti, inputs, vehicle.input_bounds)

    options = {
        'ipopt.print_level': 0,  # Minimal printing
        'ipopt.sb': 'yes'  # Silence banner header
    }

    opti.set_initial(states[0, :], ref[0, :])
    opti.set_initial(states[1, :], ref[1, :])

    opti.solver('ipopt', options)
    try:
        solution = opti.solve()
        return (solution.value(cost), solution.value(states),
                solution.value(inputs))
    except RuntimeError:
        return None


def set_objective(opti, vehicle, states, inputs, crossing_time):
    """Sets the objective for the optimization problem

    :param opti: CasADi optimization object
    :param vehicle: vehicle object involved in the optimization problem
    :param states: CasADi matrix of vehicle states
    :param inputs: CasADi matrix of vehicle inputs
    :param crossing_time: required crossing intersection time
    :return: CasADi variable for the crossing cost
    """
    state_obj = casadi.trace(casadi.mtimes(casadi.mtimes(states.T, casadi.diag(
        vehicle.preferences.state)), states))

    input_obj = casadi.trace(casadi.mtimes(casadi.mtimes(inputs.T, casadi.diag(
        vehicle.preferences.input)), inputs))

    time_obj = vehicle.preferences.time * crossing_time
    cost = time_obj + state_obj + input_obj

    opti.minimize(cost)

    return cost


def set_objective_with_ref(opti, vehicle, states, inputs, crossing_time, ref):
    """Sets the objective for the optimization problem

    :param opti: CasADi optimization object
    :param vehicle: vehicle object involved in the optimization problem
    :param states: CasADi matrix of vehicle states
    :param inputs: CasADi matrix of vehicle inputs
    :param crossing_time: required crossing intersection time
    :param ref: reference trajectory to track
    :return: CasADi variable for the crossing cost
    """
    pos_error = states[:2, :] - ref
    pos_weights = casadi.diag(vehicle.preferences.state)[:2, :2]

    path_obj = casadi.trace(
        casadi.mtimes(casadi.mtimes(pos_error.T, pos_weights), pos_error))

    input_obj = casadi.trace(casadi.mtimes(casadi.mtimes(inputs.T, casadi.diag(
        vehicle.preferences.input)), inputs))

    time_obj = vehicle.preferences.time * crossing_time
    cost = time_obj + path_obj + input_obj

    opti.minimize(cost)

    return cost


def set_bounds(opti, variable, bounds) -> None:
    """Set bounds on a decision variable

    Decision variables include vehicle states and inputs. A decision
    variable often multi-dimensional. For example, a unicycle state
    decision variable is (3 x n), where the rows are x-position,
    y-position, and heading. The n columns are for each of the n
    samples over the control horizon.

    :param opti: CasADi optimization object
    :param variable: CasADi decision variable being bounded
    :param bounds: bounds object containing variable bounds
    :return: None
    """
    assert variable.shape[0] == len(bounds.initial)

    for var in range(variable.shape[0]):
        if bounds.initial[var] is not None:
            opti.subject_to(variable[var, 0] == bounds.initial[var])
        if bounds.final[var] is not None:
            opti.subject_to(variable[var, -1] == bounds.final[var])

        lower = bounds.lower[var]
        upper = bounds.upper[var]
        if lower is not None and upper is not None:
            opti.subject_to(opti.bounded(lower, variable[var, :], upper))
        elif upper is not None:
            opti.subject_to(variable[var, :] <= upper)
        elif lower is not None:
            opti.subject_to(variable[var, :] <= lower)


def discretize(opti, vehicle, states, inputs, num_samples, sample_period):
    """Discretize vehicle's transition model over given horizon

    :param opti: CasADi optimization object
    :param vehicle: vehicle object whose model is being discretized
    :param states: CasADi matrix of vehicle states
    :param inputs: CasADi matrix of vehicle inputs
    :param num_samples: number of samples in optimization horizon
    :param sample_period: discretization sample period
    :return: None
    """
    for sample in range(num_samples):
        next_state = states[:, sample] + sample_period * \
                     vehicle.transition(states[:, sample], inputs[:, sample])
        opti.subject_to(states[:, sample + 1] == next_state)


def discretize_rk4(opti, vehicle, states, inputs, num_samples, sample_period):
    for sample in range(num_samples):
        k_1 = vehicle.transition(states[:, sample], inputs[:, sample])
        k_2 = vehicle.transition(states[:, sample] + sample_period * k_1 / 2,
                                 inputs[:, sample])
        k_3 = vehicle.transition(states[:, sample] + sample_period * k_2 / 2,
                                 inputs[:, sample])
        k_4 = vehicle.transition(states[:, sample] + sample_period * k_3,
                                 inputs[:, sample])
        next_state = states[:, sample] + sample_period/6 * (k_1 +
                                                            2 * k_2 +
                                                            2 * k_3 +
                                                            k_4)
        opti.subject_to(states[:, sample + 1] == next_state)


def get_horizon(crossing_time, num_samples=None, delta_t=None):
    """Get the control horizon parameters based

    This function calculates the missing control horizon parameter
    based on two supplied parameters. If num_samples is provides,
    delta_t is calculated and vise versa. num_samples and delta_t are
    exclusive, meaning they cannot both be provided.

    :param crossing_time: intersection crossing time (the control
    horizon duration)
    :param num_samples: number of samples in the control horizon
    :param delta_t: period between samples
    :return: either num_samples or delta_t depending on which arguments
    were provided
    """
    assert not (num_samples and delta_t), \
        "'num_samples' and 'delta_t' are exclusive; they cannot both " \
        "have a value"

    if num_samples:
        return crossing_time / num_samples

    return int(math.ceil(crossing_time / delta_t))


def get_cost_domain_indices(costs):
    lower_i = 0
    upper_i = len(costs) - 1

    for index, cost in enumerate(costs):
        # if not cost:
        if cost is not None:
            lower_i = index
            break

    for index, cost in reversed(list(enumerate(costs))):
        # if not cost:
        if cost is not None:
            upper_i = index
            break

    return lower_i, upper_i


def costs_list_to_spline(times, cost_list):
    domain_indices = get_cost_domain_indices(cost_list)
    domain = slice(domain_indices[0], domain_indices[1] + 1)
    cost_func = casadi.interpolant('cost_func', 'bspline', [times[domain]],
                                   cost_list[domain])
    cost_bounds = (times[domain_indices[0]], times[domain_indices[1]])

    return cost_func, cost_bounds


def wait_costs_to_spline(times, costs):
    cost_func = casadi.interpolant('wait_func', 'bspline', [times], costs)
    cost_bounds = (times[0], times[-1])

    return cost_func, cost_bounds
