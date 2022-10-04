"""Test module for cmd_dispatch module

"""
# Standard library imports
import unittest

# Local application imports
from autocross import cmd_dispatch


class TestCmdDispatch(unittest.TestCase):
    """Test cases for cmd_dispatch

    """
    def test_cmd_dispatcher_register_command_no_replace(self) -> None:
        """Test case for registering new command

        Test case assumes that an existing command is not
        being replaced.

        :return: None
        """
        dispatcher = cmd_dispatch.CmdDispatcher()

        try:
            dispatcher.register_command('test_cmd', lambda _: 0)
        except Exception as err:  # pylint: disable=W0703
            self.fail(f'Registering command raised exception '
                      f'unexpectedly: {err}')

    def test_cmd_dispatcher_register_command_good_replace(self) -> None:
        """Test case for re-registering a command

        Test case assumes command is successfully replacing an
        existing command.

        :return: None
        """
        dispatcher = cmd_dispatch.CmdDispatcher()

        dispatcher.register_command('test_cmd', lambda _: 0)

        try:
            dispatcher.register_command('test_cmd', lambda _: 1, replace=True)
        except Exception as err:  # pylint: disable=W0703
            self.fail(f'Registering command raised exception '
                      f'unexpectedly: {err}')

    def test_cmd_dispatcher_register_command_bad_replace(self):
        """Test case for re-registering a command

        Test case assumes command fails at replacing an
        existing command.

        :return:
        """
        dispatcher = cmd_dispatch.CmdDispatcher()

        dispatcher.register_command('test_cmd', lambda _: 0)

        with self.assertRaises(KeyError):
            dispatcher.register_command('test_cmd', lambda _: 1)

    def test_cmd_dispatcher_dispatch_good_key(self) -> None:
        """Test case for dispatching to registered command

        Test case assumes command is registered with dispatcher.

        :return: None
        """
        dispatcher = cmd_dispatch.CmdDispatcher()

        dispatcher.register_command('test_cmd', lambda _: 0)

        try:
            dispatcher.dispatch('test_cmd', None)
        except Exception as err:  # pylint: disable=W0703
            self.fail(f'Dispatching command raised exception '
                      f'unexpectedly: {err}')

    def test_cmd_dispatcher_dispatch_bad_key(self) -> None:
        """Test case for dispatching to registered command

        Test case assumes command is not registered with dispatcher.

        :return: None
        """
        dispatcher = cmd_dispatch.CmdDispatcher()

        with self.assertRaises(KeyError):
            dispatcher.dispatch('test_cmd', None)


if __name__ == '__main__':
    unittest.main()
