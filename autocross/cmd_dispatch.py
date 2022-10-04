"""Command dispatching

This module contains the command dispatcher.
"""
from typing import Any
from typing import Callable


class CmdDispatcher:
    """Command dispatcher

    This class dispatches commands and their arguments to the
    appropriate handler
    """
    def __init__(self) -> None:
        """Init function

        Initializes the command registry

        :return: None
        """
        self._registry = {}

    def register_command(self, cmd: str, handler: Callable[[Any], int],
                         replace: bool = False) -> None:
        """Register a command handler

        :param cmd: command name
        :param handler: command handler
        :param replace: replace any currently registered handler
        :return: None
        :raises: KeyError if replace is false and a handler is already
        registered
        """
        if cmd in self._registry and not replace:
            raise KeyError(f"Command '{cmd}' already has a "
                           f"registered handler")

        self._registry[cmd] = handler

    def dispatch(self, cmd: str, args: any) -> int:
        """Dispatch a command to the registered handler

        :param cmd: command name
        :param args: command arguments
        :return: exit code of called command
        """
        return self._registry[cmd](args)
