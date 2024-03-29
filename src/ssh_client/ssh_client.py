from abc import ABC, abstractmethod
from typing import Tuple


class ShellOutput:
    """
    Basic class representing an output received after executing a shell command.
    """
    def __init__(self, stdout: str, stderr: str, exit_code: int):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code


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
