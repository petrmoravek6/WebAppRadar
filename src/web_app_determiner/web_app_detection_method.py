from abc import ABC, abstractmethod
from typing import Optional

from src.web_app_determiner.web_app_determiner import WebAppInfo


class IWebAppDetectionMethod(ABC):
    @abstractmethod
    def inspect_host(self, host: str) -> Optional[WebAppInfo]:
        pass
