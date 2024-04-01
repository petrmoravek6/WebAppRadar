from abc import ABC, abstractmethod
import selenium.webdriver
import time
from src.client_side_renderer.client_side_renderer import IClientSideRenderer
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException


class SeleniumRenderer(IClientSideRenderer, ABC):
    @abstractmethod
    def _get_driver(self) -> selenium.webdriver.remote.webdriver.WebDriver:
        pass

    def __init__(self, page_load_timeout: int = 10, explicit_waiting: float = 3.0):
        self.explicit_waiting = explicit_waiting
        self.driver = self._get_driver()
        self.driver.set_page_load_timeout(page_load_timeout)

    def get_page_content(self, host: str) -> str:
        try:
            self.driver.get(host)
        except TimeoutException:
            raise ConnectionError("Timeout while waiting for page to load")
        time.sleep(self.explicit_waiting)
        page_content = self.driver.page_source
        return page_content