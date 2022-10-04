"""Vehicle module

This module contains vehicle base class, specializations, and
supporting classes.
"""
# Standard library imports
import abc
from dataclasses import dataclass
from typing import Optional, Union

# Third party imports
import casadi
import dacite


@dataclass(order=True)
class Bounds:
    """Bounds class

    """
    initial: Union[tuple[Optional[float], ...], list[Optional[float], ...]]
    """Initial bounds (at beginning of control horizon)"""
    final: Union[tuple[Optional[float], ...], list[Optional[float], ...]]
    """Final bounds (at end of control horizon)"""
    upper: Union[tuple[Optional[float], ...], list[Optional[float], ...]]
    """Upper bounds (used during control horizon)"""
    lower: Union[tuple[Optional[float], ...], list[Optional[float], ...]]
    """Lower bounds (user during control horizon)"""


@dataclass(order=True)
class Preferences:
    """Vehicle passenger preferences class

    """
    state: Union[tuple[float, ...], list[float, ...]]
    """State preferences"""
    input: Union[tuple[float, ...], list[float, ...]]
    """Input preferences"""
    time: float
    """Crossing time preference"""


class Vehicle(abc.ABC):
    @abc.abstractmethod
    def transition(self, state, input_):
        """Transition system state

        Function returns the next system state based on current
        system state and system input.

        :param state: current system state
        :param input_: current system input
        :return: next system state
        """


class UnicycleVehicle(Vehicle):
    """Vehicle that uses a unicycle kinematic model.

    """
    def __init__(self, state_bounds: Bounds, input_bounds,
                 preferences: Preferences):
        """Init function

        :param state_bounds: vehicle state bounds
        :param input_bounds: vehicle input bounds
        :param preferences: passenger preferences
        """
        super(UnicycleVehicle, self).__init__()

        self._num_states = 3
        self._num_inputs = 2
        self._state_bounds = state_bounds
        self._input_bounds = input_bounds
        self._preferences = preferences

        assert len(self._state_bounds.initial) == self._num_states
        assert len(self._state_bounds.final) == self._num_states
        assert len(self._state_bounds.upper) == self._num_states
        assert len(self._state_bounds.lower) == self._num_states

        assert len(self._input_bounds.initial) == self._num_inputs
        assert len(self._input_bounds.final) == self._num_inputs
        assert len(self._input_bounds.upper) == self._num_inputs
        assert len(self._input_bounds.lower) == self._num_inputs

        assert len(self._preferences.state) == self._num_states
        assert len(self._preferences.input) == self._num_inputs

    @property
    def num_states(self) -> int:
        """Get number of system states

        :return: number of system states
        """
        return self._num_states

    @property
    def num_inputs(self) -> int:
        """Get number of system inputs

        :return: number of system inputs
        """
        return self._num_inputs

    @property
    def state_bounds(self) -> Bounds:
        """Get system state bounds

        :return: system state bounds
        """
        return self._state_bounds

    @property
    def input_bounds(self) -> Bounds:
        """Get system input bounds

        :return: system input bounds
        """
        return self._input_bounds

    @property
    def preferences(self) -> Preferences:
        """Get user preferences

        :return: user preferences
        """
        return self._preferences

    def transition(self, state, input_):
        """Calculate new system state from current state and input

        :param state: current system state
        :param input_: curren system input
        :return: new system state
        """
        d_x_pos = input_[1] * casadi.cos(state[2])
        d_y_pos = input_[1] * casadi.sin(state[2])
        d_heading = input_[0]

        return casadi.vertcat(d_x_pos, d_y_pos, d_heading)


def build_vehicle(data: dict) -> Vehicle:
    state_bounds = dacite.from_dict(Bounds, data['state_bounds'])
    input_bounds = dacite.from_dict(Bounds, data['input_bounds'])
    preferences = dacite.from_dict(Preferences, data['preferences'])

    return UnicycleVehicle(state_bounds, input_bounds, preferences)
