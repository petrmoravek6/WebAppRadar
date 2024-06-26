from abc import ABC, abstractmethod


class IVhostsCmds(ABC):
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
    def get_content_from_server(self) -> str:
        """
        Query used for getting necessary information for getting all virtual hosts on a server
        """
        pass

    @abstractmethod
    def get_all_vhosts_from_content(self, content: str) -> set[str]:
        """
        Process output from content parameter (ideally from 'get_content_from_server' method) and return all unique
        virtual hosts
        :param content: content to be processed
        :return: set of virtual hosts server names parsed from the input
        """
        pass
