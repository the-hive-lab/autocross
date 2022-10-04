import unittest
import random

from autocross import schedule


class TestCrossingSchedule(unittest.TestCase):
    """Test cases for generating crossing schedules

    """
    def test_scheduled_random(self):
        """Test case for random schedule

        For reproducibility, the random number generator is seeded with
        a constant value. The seed value is also passed into the function,
        which uses a random shuffle internally

        :return: None
        """
        random_seed = 42
        random.seed(random_seed)

        num_vehicles = 10
        sol = list(range(num_vehicles))
        random.shuffle(sol)

        output = schedule.scheduled_random(num_vehicles, random_seed)

        self.assertEqual(sol, output)

    def test_scheduled_first_come_first_serve(self):
        """Test case for first-come-first-server schedule

        :return: None
        """
        arrival_times = [23, 51, 0, 30]
        sol = [1, 3, 0, 2]

        output = schedule.scheduled_first_come_first_serve(arrival_times)

        self.assertEqual(sol, output)

    def test_scheduled_fastest_crossing_first(self):
        """Test case for fastest-crossing-fist schedule

        :return: None
        """
        crossing_times = [54, 1, 34, 9, 5]
        sol = [4, 0, 3, 2, 1]

        output = schedule.scheduled_fastest_crossing_first(crossing_times)

        self.assertEqual(sol, output)


if __name__ == '__main__':
    unittest.main()
