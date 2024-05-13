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
        res2 = self.det.detect_web_app_info("grafana.webappradar-example.io")
        res3 = self.det.detect_web_app_info("bareos.webappradar-example.io")
        res4 = self.det.detect_web_app_info("keycloak.webappradar-example.io")
        res5 = self.det.detect_web_app_info("gitlab.webappradar-example.io")
        res6 = self.det.detect_web_app_info("prometheus.webappradar-example.io")
        res7 = self.det.detect_web_app_info("snipe-it.webappradar-example.io")
        res8 = self.det.detect_web_app_info("teamcity.webappradar-example.io")
        res9 = self.det.detect_web_app_info("www.google.com")

        expected1 = WebAppInfo("Atlassian Jira", "9.4.18")
        expected2 = WebAppInfo("Grafana", "10.1.1")
        expected3 = WebAppInfo("Bareos", "17.2.4")
        expected4 = WebAppInfo("Keycloak", "22.0.3")
        expected5 = WebAppInfo("GitLab", "16.8.5")
        expected6 = WebAppInfo("Prometheus", "2.14.0")
        expected7 = WebAppInfo("Snipe-IT", "6.0.8")
        expected8 = WebAppInfo("TeamCity", "2023.11.3")
        expected9 = None  # Google not on list of known web apps

        self.assertEqual(res1, expected1)
        self.assertEqual(res2, expected2)
        self.assertEqual(res3, expected3)
        self.assertEqual(res4, expected4)
        self.assertEqual(res5, expected5)
        self.assertEqual(res6, expected6)
        self.assertEqual(res7, expected7)
        self.assertEqual(res8, expected8)
        self.assertEqual(res9, expected9)

    def test_discover_invalid_hosts(self):
        res1 = self.det.detect_web_app_info("http://420.webappradar-example.io")
        res2 = self.det.detect_web_app_info("64sd5f6sd4f65d4sf")

        expected1 = None
        expected2 = None

        self.assertEqual(res1, expected1)
        self.assertEqual(res2, expected2)
