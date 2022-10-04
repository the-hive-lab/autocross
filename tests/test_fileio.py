"""Test cases for fileio module

"""

# Standard library imports
import os
import pickle
import random
import time
import unittest

# Local application imports
from autocross import fileio


class TestFileio(unittest.TestCase):
    """Test cases for reading, writing, and parsing files.

    """
    def setUp(self) -> None:
        """Setup cost filepath and cost data

        Cost data variable is test data used to verify the parsing
        function. The cost data is pickled and stored in the location
        specified by the filepath variable. Pickled data is then used
        as test against the file reader.

        :return: None
        """
        self._cost_filepath = str(time.time()) + str(random.randint(0, 100))

        self._cost_data = {
            'cost_function': 'function_repr',
            'cost_bounds': (1, 2)
        }

    def tearDown(self) -> None:
        """Tear down any testing stuff

        Removes the test cost data filepath if it exists.

        :return: None
        """
        if os.path.exists(self._cost_filepath):
            os.remove(self._cost_filepath)

    def test_read_cost_file(self) -> None:
        """Test case for reading the test cost file

        :return: None
        """
        with open(self._cost_filepath, 'wb') as file:
            pickle.dump(self._cost_data, file)

        output = fileio.read_cost_file(self._cost_filepath)

        self.assertEqual(self._cost_data, output)

    def test_write_cost_file(self) -> None:
        """Test case for writing cost file

        :return: None
        """
        data = {
            'cost_function': 'my_func',
            'cost_bounds': (1, 2)
        }
        filepath = str(time.time()) + str(random.randint(0, 100))

        try:
            with open(filepath, 'wb') as file:
                pickle.dump(data, file)

            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as err:  # pylint: disable=W0703
            self.fail(f'Dumping pickle raised exception unexpectedly: {err}')

    def test_parse_cost_data(self) -> None:
        """Test case for parsing the cost data

        :return: None
        """
        out_func, out_bounds = fileio.parse_cost_data(self._cost_data)

        self.assertEqual(self._cost_data['cost_function'], out_func)
        self.assertEqual(self._cost_data['cost_bounds'], out_bounds)

    def test_read_vehicle_file(self) -> None:
        """Test case for reading a vehicle file

        :return: None
        """
        filepath = 'data/test.vehicle'
        expected = {
            'model': {
                'type': 'test',
                'params': None
            },
            'state_bounds': {
                'initial': {
                    'state': 42
                },
                'final': {
                    'state': 42
                },
                'upper': {
                    'state': 42
                },
                'lower': {
                    'state': 42
                }
            },
            'input_bounds': {
                'initial': {
                    'input': 42
                },
                'final': {
                    'input': 42
                },
                'upper': {
                    'input': 42
                },
                'lower': {
                    'input': 42
                }
            },
            'preferences': {
                'state_weights': {
                    'state': 42,
                },
                'input_weights': {
                    'input': 42,
                },
                'time_weight': 42
            }
        }

        output = fileio.read_vehicle_file(filepath)

        self.assertIsInstance(output, dict)
        self.assertEqual(expected, output)


if __name__ == '__main__':
    unittest.main()
