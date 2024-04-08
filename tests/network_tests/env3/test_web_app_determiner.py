import os
import unittest

from src.web_app_determiner.html_content_parsing_method import HTMLContentParsingFromFileMethod
from src.web_app_determiner.web_app_determiner import WebAppDeterminer
from src.client_side_renderer.selenium_chrome_renderer import SeleniumChromeRenderer
from src.web_app_determiner.web_app_info import WebAppInfo
from src.web_app_determiner.web_app_rule.authentication.auth_executor import AuthExecutor
from src.web_app_determiner.web_app_rule.json_deserializer import JsonWebAppRulesDeserializer


class TestWebAppDeterminer(unittest.TestCase):
    """Integration tests for TestWebAppDeterminer combined with HTMLContentParsingFromFileMethod"""
    def setUp(self):
        web_apps_json_path = os.path.join(os.path.dirname(__file__), 'web-apps.json')
        renderer = SeleniumChromeRenderer()
        det_methods = [HTMLContentParsingFromFileMethod(renderer,
                                                        AuthExecutor(renderer),
                                                        web_apps_json_path,
                                                        JsonWebAppRulesDeserializer())]
        self.resolver = WebAppDeterminer(det_methods)

    def test_discover_vhosts(self):
        res1 = self.resolver.detect_web_app_info("http://jira.webappradar-example.io")
        res2 = self.resolver.detect_web_app_info("grafana.webappradar-example.io")
        res3 = self.resolver.detect_web_app_info("bareos.webappradar-example.io")
        res4 = self.resolver.detect_web_app_info("keycloak.webappradar-example.io")

        expected1 = WebAppInfo("Atlassian Jira", "9.4.18")
        expected2 = WebAppInfo("Grafana", "10.1.1")
        expected3 = WebAppInfo("Bareos", "17.2.4")
        expected4 = WebAppInfo("Keycloak", "22.0.3")

        self.assertEqual(res1, expected1)
        self.assertEqual(res2, expected2)
        self.assertEqual(res3, expected3)
        self.assertEqual(res4, expected4)
