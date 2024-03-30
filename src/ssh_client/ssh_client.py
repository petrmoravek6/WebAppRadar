from abc import ABC, abstractmethod
from typing import NamedTuple


class ShellOutput(NamedTuple):
    """
    Basic immutable structure representing an output received after executing a shell command.
    """
    stdout: str
    stderr: str
    exit_code: int


class ISSHClient(ABC):
    @abstractmethod
    def connect(self, host: str, user: str) -> None:
        """
        Connects to given host and user
        :param host: hostname or ip address to connect to
        :param user: username used for the connection
        """
        pass

    @abstractmethod
    def exec_command(self, command: str) -> ShellOutput:
        """
        Executes given command in string form
        :param command: command to execute
        :return: output received after executing the command
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Call this method to correctly close the connection. If the connection hasn't been established, this method
        should throw an exception
        """
        pass
