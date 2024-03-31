from src.client_side_renderer.selenium_renderer import SeleniumRenderer
import selenium
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options


class SeleniumChromeRenderer(SeleniumRenderer):
    def _get_driver(self) -> selenium.webdriver.remote.webdriver.WebDriver:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--incognito")
        return webdriver.Chrome(options=chrome_options)
