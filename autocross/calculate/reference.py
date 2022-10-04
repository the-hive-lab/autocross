import numpy as np


def left_turn(num_steps, radius):
    x_pos = np.linspace(0, radius, num_steps)
    y_pos = np.subtract(radius, np.sqrt(radius ** 2 - np.square(x_pos)))

    return np.stack((x_pos, y_pos))


def right_turn(num_steps, radius):
    x_pos = np.linspace(0, radius, num_steps)
    y_pos = np.subtract(np.sqrt(radius ** 2 - np.square(x_pos)), radius)

    return np.stack((x_pos, y_pos))


def straight_turn(num_steps, distance):
    x_pos = np.linspace(0, distance, num_steps)
    y_pos = np.zeros_like(x_pos)

    return np.stack((x_pos, y_pos))
