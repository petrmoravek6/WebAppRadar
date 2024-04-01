import unittest
from src.client_side_renderer.selenium_chrome_renderer import SeleniumChromeRenderer


class TestGetPageContentRealHTTPCalls(unittest.TestCase):

    def test_get_page_content_from_google(self):
        scraper = SeleniumChromeRenderer(explicit_waiting=1.5)

        test_url = 'https://www.google.com'
        page_content = scraper.get_page_content(test_url)

        self.assertIsNotNone(page_content)
        self.assertIn('google', page_content)  # Very basic validation of HTML content

    def test_get_page_content_invalid_url(self):
        scraper = SeleniumChromeRenderer(explicit_waiting=1)

        test_url1 = '-test-'
        test_url2 = 'https://www.a6s6d6asd61asda4wsddgsfd5as4d5-asd5sad5asd5-asd5-kyblik.sadasd.asdasd.org'

        self.assertRaises(ConnectionError, scraper.get_page_content, test_url1)
        self.assertRaises(ConnectionError, scraper.get_page_content, test_url2)
