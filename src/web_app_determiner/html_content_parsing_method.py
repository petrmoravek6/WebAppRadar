from typing import Optional
from src.web_app_determiner.web_app_detection_method import IWebAppDetectionMethod
from abc import ABC, abstractmethod
from src.web_app_determiner.web_app_determiner import WebAppInfo


class HtmlContentParsingMethod(IWebAppDetectionMethod, ABC):
    @abstractmethod
    def get_full_page_content(self):
        """
        Todo mention client side rendering
        """
        pass

    def inspect_host(self, host: str) -> Optional[WebAppInfo]:
        pass  # todo
