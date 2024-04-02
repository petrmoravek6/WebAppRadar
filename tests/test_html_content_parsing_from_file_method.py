import os
import unittest
from unittest.mock import patch, MagicMock
from src.client_side_renderer.client_side_renderer import IClientSideRenderer
from src.exceptions import FatalError
from src.web_app_determiner.web_app_info import WebAppInfo
from src.web_app_determiner.html_content_parsing_method import HTMLContentParsingFromFileMethod
from src.web_app_determiner.web_app_rule.json_deserializer import JsonWebAppRuleDeserializer


class TestHtmlContentParsingMethod(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html_contents = {
            'confluence.example.org': cls._load_html_content('tests/assets/confluence-main-page.html'),
            'jira.example.org': cls._load_html_content('tests/assets/jira-main-page.html'),
            'artifactory.example.org': cls._load_html_content('tests/assets/artifactory-main-page.html'),
            'unknown.example.org': cls._load_html_content('tests/assets/not-jira-main-page.html'),
            'prometheus.example.org': cls._load_html_content('tests/assets/prometheus-main-page.html'),
            'prometheus.example.org/status': cls._load_html_content('tests/assets/prometheus-status-page.html'),
            'bareos.example.org': cls._load_html_content('tests/assets/bareos-main-page.html'),
            'grafana.example.org': cls._load_html_content('tests/assets/grafana-main-page.html'),
            'teamcity.example.org': cls._load_html_content('tests/assets/teamcity-main-page.html'),
            'testrail.example.org': cls._load_html_content('tests/assets/testrail-main-page.html'),
            'notfound.example.org': None
        }

    @classmethod
    def _load_html_content(cls, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()

    def test_wrong_file(self):
        self.assertRaises(FatalError, HTMLContentParsingFromFileMethod, MagicMock, "", MagicMock)
        self.assertRaises(FatalError, HTMLContentParsingFromFileMethod, MagicMock, "..", MagicMock)
        self.assertRaises(FatalError,
                          HTMLContentParsingFromFileMethod,
                          MagicMock,
                          os.path.join(os.path.dirname(__file__), "tests", "test_html_content_parsing_from_file_method.py"),
                          MagicMock)

    @patch.object(HTMLContentParsingFromFileMethod, '_get_full_page_content')
    def test_inspect_host(self, mock_get_full_page_content):
        mock_client = MagicMock(spec=IClientSideRenderer)
        json_deserializer = JsonWebAppRuleDeserializer()
        method = HTMLContentParsingFromFileMethod(mock_client,
                                                  os.path.join(os.path.dirname(__file__),
                                                               "assets",
                                                               "web-apps.json"),
                                                  json_deserializer)

        # Use the preloaded HTML content for the mock side effect
        mock_get_full_page_content.side_effect = lambda host: self.html_contents.get(host)

        result_confluence = method.inspect_host('confluence.example.org')
        result_jira = method.inspect_host('jira.example.org')
        result_artifactory = method.inspect_host('artifactory.example.org')
        result_bareos = method.inspect_host('bareos.example.org')
        result_grafana = method.inspect_host('grafana.example.org')
        result_prometheus = method.inspect_host('prometheus.example.org')
        result_teamcity = method.inspect_host('teamcity.example.org')
        result_testrail = method.inspect_host('testrail.example.org')

        result_unknown_webapp = method.inspect_host('unknown.example.org')
        result_page_not_found = method.inspect_host('notfound.example.org')

        self.assertEqual(WebAppInfo("Atlassian Confluence", "8.5.7"), result_confluence)
        self.assertEqual(WebAppInfo("Atlassian Jira", "9.4.18"), result_jira)
        self.assertEqual(WebAppInfo("JFrog Artifactory Pro", "7.24.3"), result_artifactory)
        self.assertEqual(WebAppInfo("Bareos", "17.2.4"), result_bareos)
        self.assertEqual(WebAppInfo("Grafana", "10.1.1"), result_grafana)
        self.assertEqual(WebAppInfo("Prometheus", "2.14.0"), result_prometheus)
        self.assertEqual(WebAppInfo("TeamCity", "2023.11.3"), result_teamcity)
        self.assertEqual(WebAppInfo("TestRail", "8.0.1"), result_testrail)
        self.assertEqual(None, result_unknown_webapp)
        self.assertEqual(None, result_page_not_found)
