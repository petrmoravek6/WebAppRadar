from src.client_side_renderer.selenium_renderer import SeleniumRenderer
import selenium
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class SeleniumChromeRenderer(SeleniumRenderer):
    def _get_driver(self) -> selenium.webdriver.remote.webdriver.WebDriver:
        return webdriver.Chrome()
