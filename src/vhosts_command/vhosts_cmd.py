from abc import ABC, abstractmethod


class VhostsCmd(ABC):
    """
    Interface representing string commands used for querying on Linux based machines.
    These queries are used for searching virtual hosts.
    Each of the subclass of this interface should represent concrete web server.
    """
    @abstractmethod
    def is_web_server_running(self) -> str:
        """
        Query used for checking if the web server is running
        """
        pass

    @abstractmethod
    def get_all_vhosts(self) -> str:
        """
        Query used for getting all virtual hosts of the web server
        """
        pass
