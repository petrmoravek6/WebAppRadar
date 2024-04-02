import os
from abc import abstractmethod
from typing import Optional, Iterable, Collection
from src.exceptions import FatalError
from src.web_app_determiner.web_app_detection_method import IWebAppDetectionMethod
from src.client_side_renderer.selenium_renderer import SeleniumRenderer
from src.web_app_determiner.web_app_info import WebAppInfo
import logging


from src.web_app_determiner.web_app_rule.web_app_rule import WebAppRule

logger = logging.getLogger(__name__)


class HtmlContentParsingMethod(IWebAppDetectionMethod):
    def __init__(self, client: SeleniumRenderer):
        self.client = client

    def _get_full_page_content(self, host: str) -> Optional[str]:
        """
        Todo mention client side rendering
        """
        try:
            return self.client.get_page_content(host)
        except ConnectionError as ce:
            logger.error(f"Connection error during loading page '{host}'. {ce}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during loading page '{host}'. {e}")
            return None

    @abstractmethod
    def _get_web_app_rules(self) -> Iterable[WebAppRule]:
        pass

    def inspect_host(self, host: str) -> Optional[WebAppInfo]:
        web_app_rules = self._get_web_app_rules()
        page_content = self._get_full_page_content(host)
        if not page_content:
            return None
        for rule in web_app_rules:
            if rule.matches(page_content):
                name = rule.name
                if rule.auth:
                    page_content = rule.auth.accept(self.client.driver)
                    if page_content is None:
                        return WebAppInfo(name, None)
                if rule.version_path:
                    page_content = self._get_full_page_content(host + rule.version_path)
                ver = None
                if page_content:
                    ver = rule.find_version(page_content)
                return WebAppInfo(name, ver)
        return None

    def _authenticate(self) -> None:
        raise NotImplementedError()


class HTMLContentParsingFromFileMethod(HtmlContentParsingMethod):
    from src.web_app_determiner.web_app_rule.deserializer import IWebAppRuleDeserializer
    def __init__(self, client: SeleniumRenderer, file_path: str, deserializer: IWebAppRuleDeserializer):
        super().__init__(client)
        self.rules = HTMLContentParsingFromFileMethod._load_rules(file_path, deserializer)

    def _get_web_app_rules(self) -> Iterable[WebAppRule]:
        return self.rules

    @staticmethod
    def _load_rules(file_path: str, deserializer: IWebAppRuleDeserializer) -> Collection[WebAppRule]:
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            raise FatalError(f"The path for web app rules: '{file_path}' is not valid or does not exist.",
                             "Please check the file exists and is not a folder")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
            try:
                return deserializer.deserialize(data)
            except Exception as e:
                raise FatalError(f"Error during deserialization of file at: '{file_path}'"
                                 f". Please check the file is in the correct format.",
                                 str(e))
