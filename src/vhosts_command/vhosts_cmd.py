from abc import ABC, abstractmethod


class VhostsCmd(ABC):
    @abstractmethod
    def is_web_server_running(self) -> str:
        pass

    @abstractmethod
    def get_all_vhosts(self) -> str:
        pass
