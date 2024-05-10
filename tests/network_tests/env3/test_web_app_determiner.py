import os
import unittest

from src.web_app_determiner.html_content_parsing_method import HTMLContentParsingFromFileMethod
from src.web_app_determiner.web_app_determiner import WebAppDeterminer
from src.client_side_renderer.selenium_chrome_renderer import SeleniumChromeRenderer
from src.web_app_determiner.web_app_info import WebAppInfo
from src.web_app_determiner.web_app_rule.authentication.auth_executor import AuthExecutor
from src.web_app_determiner.web_app_rule.json_deserializer import JsonWebAppRulesDeserializer


class TestWebAppDeterminer(unittest.TestCase):
    """Integration/system tests for TestWebAppDeterminer combined with HTMLContentParsingFromFileMethod"""
    def setUp(self):
        web_apps_json_path = os.path.join(os.path.dirname(__file__), 'web-apps.json')
        renderer = SeleniumChromeRenderer()
        det_methods = [HTMLContentParsingFromFileMethod(renderer,
                                                        AuthExecutor(renderer),
                                                        web_apps_json_path,
                                                        JsonWebAppRulesDeserializer())]
        self.det = WebAppDeterminer(det_methods)

    def test_discover_valid_hosts(self):
        res1 = self.det.detect_web_app_info("http://jira.webappradar-example.io")
        res3 = self.det.detect_web_app_info("bareos.webappradar-example.io")
        res9 = self.det.detect_web_app_info("www.google.com")

        expected1 = WebAppInfo("Atlassian Jira", "9.4.18")
        expected3 = WebAppInfo("Bareos", "17.2.4")
        expected9 = None  # Google not on list of known web apps

        self.assertEqual(res1, expected1)
        self.assertEqual(res3, expected3)
        self.assertEqual(res9, expected9)

    def test_discover_invalid_hosts(self):
        res1 = self.det.detect_web_app_info("http://420.webappradar-example.io")
        res2 = self.det.detect_web_app_info("64sd5f6sd4f65d4sf")

        expected1 = None
        expected2 = None

        self.assertEqual(res1, expected1)
        self.assertEqual(res2, expected2)
