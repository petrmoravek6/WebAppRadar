import os
from abc import abstractmethod, ABC
from typing import Optional, Iterable, Collection
from src.exceptions import FatalError
from src.web_app_determiner.web_app_detection_method import IWebAppDetectionMethod
from src.client_side_renderer.selenium_renderer import SeleniumRenderer
from src.web_app_determiner.web_app_info import WebAppInfo
import logging
from src.web_app_determiner.web_app_rule.authentication.auth import IAuthVisitor
from src.web_app_determiner.web_app_rule.deserializer import IWebAppRulesDeserializer
from src.web_app_determiner.web_app_rule.web_app_rule import WebAppRule

logger = logging.getLogger(__name__)


class HtmlContentParsingMethod(IWebAppDetectionMethod, ABC):
    """This is a web app detection method that extracts information from loaded HTML content of the web app pages. It looks for specific elements on specific relative paths defined in the _get_web_app_rules abstract method. It uses SeleniumRenderer for client side content loading and IAuthExecutor for page authentication."""
    def __init__(self, client: SeleniumRenderer, auth_executor: IAuthVisitor):
        self.client = client
        self.auth_executor = auth_executor

    def _get_full_page_content(self, host: str) -> Optional[str]:
        """
        Private method used for getting a full HTML content of the web app on a given host
        :param host: domain name
        :return: fully loaded page content of the host
        """
        if not host.startswith('http://') and not host.startswith('https://'):
            host = f'http://{host}'
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
        """
        Defines a way to get the web app rules (instances of WebAppRule) used during page content discovery
        """
        pass

    def inspect_host(self, host: str) -> Optional[WebAppInfo]:
        web_app_rules = self._get_web_app_rules()
        page_content = self._get_full_page_content(host)
        if not page_content:
            return None
        for rule in web_app_rules:
            if rule.matches(page_content):
                name = rule.web_app_name
                if rule.auth:
                    page_content = rule.auth.accept(self.auth_executor)
                    if page_content is None:
                        logger.error(f"Authentication to {name} on '{host}' was not successful. Please check the provided credentials and locators.")
                        return WebAppInfo(name, None)
                if rule.version_path:
                    ful_ver_path = host + rule.version_path
                    page_content = self._get_full_page_content(ful_ver_path)
                    if page_content is None:
                        logger.error(f"Couldn't visit {ful_ver_path} for {name}'s version. Please check the set 'version_path' and 'version' for {name}")
                        return WebAppInfo(name, None)
                ver = None
                if page_content:
                    ver = rule.find_version(page_content)
                logger.info(f"{name} ({ver if ver else 'unknown'}) running on {host}")
                return WebAppInfo(name, ver)
        logger.info(f"{host} was not matched with any known web application")
        return None


class HTMLContentParsingFromFileMethod(HtmlContentParsingMethod):
    """This class implements the HtmlContentParsingMethod's method _get_web_app_rules that it loads the rules from file. You can choose the file format by suppliing specific deserializer in the constructor."""
    def __init__(self, client: SeleniumRenderer, auth_executor: IAuthVisitor,
                 file_path: str, deserializer: IWebAppRulesDeserializer):
        super().__init__(client, auth_executor)
        self.rules = HTMLContentParsingFromFileMethod._load_rules(file_path, deserializer)

    def _get_web_app_rules(self) -> Iterable[WebAppRule]:
        return self.rules

    @staticmethod
    def _load_rules(file_path: str, deserializer: IWebAppRulesDeserializer) -> Collection[WebAppRule]:
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
