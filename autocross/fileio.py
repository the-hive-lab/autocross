# Standard library imports
import pickle
import os

# Third party imports
import yaml


def get_file_name(filepath: str) -> str:
    file = os.path.basename(filepath)
    filename, _ = os.path.splitext(file)

    return filename


def get_file_extension(filepath: str) -> str:
    file = os.path.basename(filepath)
    _, extension = os.path.splitext(file)

    return extension


def get_file_directory(filepath: str) -> str:
    return os.path.dirname(filepath)


def read_cost_file(filepath: str) -> dict:
    """Read cost data from file

    File is assumed to be in the Python pickle format. Data is read in
    from the file and returned as a dict.

    :param filepath: path to the pickle file containing the cost data
    :return: dict with the cost function and function bounds
    """
    with open(filepath, 'rb') as file:
        data = pickle.load(file)

    assert isinstance(data, dict)

    return data


def write_cost_file(filepath: str, func, bounds) -> None:
    """Write cost data to file

    :param filepath: path to the pickle file containing the cost data
    :param func: cost function to save
    :param bounds: cost bounds to save
    :return: None
    """
    data = {
        'cost_function': func,
        'cost_bounds': bounds
    }

    with open(filepath, 'wb') as file:
        pickle.dump(data, file)


def parse_cost_data(data: dict) -> tuple:
    """Parse cost data from dict

    This function extracts the two necessary data to fully represent
    a vehicle's cost: the cost function, and the cost bounds. It is
    assumed that the dict contains 'cost_function' and 'cost_bounds'
    keys.

    :param data: vehicle cost data. Assumed that data contains a cost
    function that is a CasADi `interpolant` object. Also assumed that
    data contains a cost bounds that is a tuple.
    :return: tuple containing the cost function and cost bounds
    """
    assert 'cost_function' in data, "Key 'cost_function' not found in data"
    assert 'cost_bounds' in data, "Key 'cost_bounds' not found in data"

    return data['cost_function'], data['cost_bounds']


def read_vehicle_file(filepath: str) -> dict:
    """Reade vehicle data from file

    File is assumed to be in YAML format.

    :param filepath: path to the vehicle file
    :return: dict with the vehicle data
    """
    with open(filepath, 'r') as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)

    assert isinstance(data, dict)

    return data


def read_system_file(filepath: str) -> dict:
    with open(filepath, 'rb') as file:
        data = pickle.load(file)

    assert isinstance(data, dict)

    return data


def write_system_file(filepath: str, states, inputs, **kwargs):
    data = {
        'states': states,
        'inputs': inputs,
        **kwargs
    }

    with open(filepath, 'wb') as file:
        pickle.dump(data, file)


def parse_system_data(data: dict) -> tuple:
    assert 'states' in data, "Key 'states' not found in data"
    assert 'inputs' in data, "Key 'inputs' not found in data"

    return data['states'], data['inputs']


def write_schedule_file(filepath: str, order: list, times: list):
    data = {
        'crossing_order': order,
        'crossing_times': times
    }

    with open(filepath, 'wb') as file:
        pickle.dump(data, file)


def read_schedule_file(filepath: str) -> dict:
    """Read schedule data from file

    File is assumed to be in the Python pickle format. Data is also
    assumed to be stored as a Python dict.

    :param filepath: filepath to the pickle file containing the data
    :return: dict with schedule data (crossing order and times)
    """
    with open(filepath, 'rb') as f:
        data = pickle.load(f)

    assert isinstance(data, dict)

    return data


def parse_schedule_data(data: dict) -> tuple:
    """Parse schedule data form dict

    Function extracts two necessary data to represent a crossing
    schedule: the crossing order and the crossing times. It is assumed
    that the dict contains the keys 'crossing_order' and
    'crossing_times'.

    :param data: dict containing the crossing schedule data
    :return: tuple containing the crossing order and times
    """
    assert 'crossing_order' in data, "Key 'crossing_order' not found in data"
    assert 'crossing_times' in data, "Key 'crossing_times' not found in data"

    return data['crossing_order'], data['crossing_times']
