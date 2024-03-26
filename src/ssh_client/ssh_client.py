from abc import ABC, abstractmethod
from typing import Tuple


class ISSHClient(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def exec_command(self, command: str) -> Tuple[str, str]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
