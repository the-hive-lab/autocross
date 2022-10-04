"""Test cases for vehicle module

"""
# Standard library imports
import unittest

# Local application imports
from autocross.calculate import vehicle


class VehicleTestCase(unittest.TestCase):
    def test_init_raises_error(self) -> None:
        with self.assertRaises(TypeError):
            _ = vehicle.Vehicle()


class UnicycleVehicleTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._state_bounds = vehicle.Bounds(initial=(1, 2, 3),
                                            final=(4, 5, 6),
                                            upper=(7, 8, 9),
                                            lower=(10, 11, 12))
        self._input_bounds = vehicle.Bounds(initial=(1, 2),
                                            final=(3, 4),
                                            upper=(5, 6),
                                            lower=(7, 8))
        self._preferences = vehicle.Preferences(state=(1, 2, 3),
                                                input=(4, 5),
                                                time=6)

        self._vehicle = vehicle.UnicycleVehicle(self._state_bounds,
                                                self._input_bounds,
                                                self._preferences)

    def test_num_states(self) -> None:
        self.assertEqual(self._vehicle.num_states, 3)

    def test_num_inputs(self) -> None:
        self.assertEqual(self._vehicle.num_inputs, 2)

    def test_state_bounds(self) -> None:
        self.assertEqual(self._state_bounds, self._vehicle.state_bounds)

    def test_input_bounds(self) -> None:
        self.assertEqual(self._input_bounds, self._vehicle.input_bounds)

    def test_preferences(self) -> None:
        self.assertEqual(self._preferences, self._vehicle.preferences)

    def test_transition(self) -> None:
        current_state = (0, 0, 0)
        current_input = (0, 1)
        next_state = (1, 0, 0)

        output = self._vehicle.transition(current_state, current_input)
        self.assertEqual(len(next_state), output.shape[0])

        for index, elem in enumerate(next_state):
            self.assertEqual(elem, output[index])


if __name__ == '__main__':
    unittest.main()
