from abc import ABC, abstractmethod
from typing import Tuple


class ShellOutput:
    def __init__(self, stdout: str, stderr: str, exit_code: int):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code


class ISSHClient(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def exec_command(self, command: str) -> ShellOutput:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
