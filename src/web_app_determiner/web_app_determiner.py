from abc import ABC, abstractmethod
from typing import NamedTuple, Optional


class WebAppInfo(NamedTuple):
    name: str
    version: str


class WebAppDeterminer(ABC):
    @abstractmethod
    def detect_webapp_info(self, host: str) -> Optional[WebAppInfo]:
        """
        Checks the given host for known web apps and returns every possible information it can get about a possible web app that is running on the host
        :param host: Hostname or IP address in string format
        :return: Information about the web app running on the host. If no known web app is running on the given host, return None
        """
        pass
