from typing import Optional, NamedTuple, Iterable

from src.web_app_determiner.web_app_detection_method import IWebAppDetectionMethod


class WebAppInfo(NamedTuple):
    name: str
    version: Optional[str]


class WebAppDeterminer:
    def __init__(self, detection_methods: Iterable[IWebAppDetectionMethod]):
        self.detection_methods = detection_methods

    def detect_web_app_info(self, host: str) -> Optional[WebAppInfo]:
        """
        Checks the given host for known web apps and returns every possible information it can get about a possible web app that is running on the host
        :param host: Hostname or IP address in string format
        :return: Information about the web app running on the host. If no known web app is running on the given host, return None
        """
        res = None
        for detection_method in self.detection_methods:
            info = detection_method.inspect_host(host)
            if info is not None:
                return info
        return None
