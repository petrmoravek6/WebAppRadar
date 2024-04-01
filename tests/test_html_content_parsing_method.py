import unittest
from typing import Iterable
from unittest.mock import patch, MagicMock
from src.client_side_renderer.client_side_renderer import IClientSideRenderer
from src.web_app_determiner.web_app_info import WebAppInfo
from src.web_app_determiner.web_app_rule import WebAppRule
from src.web_app_determiner.html_content_parsing_method import HtmlContentParsingMethod


class MockHtmlContentParsingMethod(HtmlContentParsingMethod):
    """
    This is a class that corresponds to HtmlContentParsingMethod with dummy implementation of abstract class which will be mocked anyway
    """
    def __init__(self, client: IClientSideRenderer):
        super().__init__(client)

    def _get_web_app_rules(self) -> Iterable[WebAppRule]:
        raise NotImplementedError()


def _load_html_content(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()


# Mock WebAppRules
mock_web_app_rules = [
    WebAppRule(name="Atlassian Jira",
               identifier="<meta name=\"application-name\" content=\"JIRA\" data-name=\"jira\"",
               version_path=None,
               version="<meta name=\"application-name\" content=\"JIRA\" data-name=\"jira\" data-version=\"(\\d+\\.\\d+\\.\\d+)\""),
    WebAppRule(name="Atlassian Confluence",
               identifier="<a href=\"https://www.atlassian.com/software/confluence\" class=\"hover-footer-link\" rel=\"nofollow\">Atlassian Confluence</a>",
               version_path=None,
               version="<span id=\"footer-build-information\">(\\d+\\.\\d+\\.\\d+)</span>"),
    WebAppRule(name="JFrog Artifactory Pro",
               identifier="<img class=\"logo-picture\" alt=\"Artifactory\"",
               version_path=None,
               version="<div class=\"wrapper-footer-data ng-binding\">\\s*Artifactory Professional<br>\\s*(\\d+\\.\\d+\\.\\d+) rev")
]


class TestHtmlContentParsingMethod(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.html_contents = {
            'confluence.example.org': cls._load_html_content('tests/assets/confluence-main-page.html'),
            'jira.example.org': cls._load_html_content('tests/assets/jira-main-page.html'),
            'artifactory.example.org': cls._load_html_content('tests/assets/artifactory-main-page.html'),
            'unknown.example.org': cls._load_html_content('tests/assets/not-jira-main-page.html')
        }

    @classmethod
    def _load_html_content(cls, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()

    @patch.object(MockHtmlContentParsingMethod, '_get_web_app_rules', return_value=mock_web_app_rules)
    @patch.object(MockHtmlContentParsingMethod, '_get_full_page_content')
    def test_inspect_host(self, mock_get_full_page_content, mock_get_web_app_rules):
        mock_client = MagicMock(spec=IClientSideRenderer)
        detector = MockHtmlContentParsingMethod(client=mock_client)

        # Use the preloaded HTML content for the mock side effect
        mock_get_full_page_content.side_effect = lambda host: self.html_contents.get(host)

        result_confluence = detector.inspect_host('confluence.example.org')
        result_jira = detector.inspect_host('jira.example.org')
        result_artifactory = detector.inspect_host('artifactory.example.org')

        self.assertEqual(WebAppInfo("Atlassian Confluence", "8.5.7"), result_confluence)
        self.assertEqual(WebAppInfo("Atlassian Jira", "9.4.18"), result_jira)
        self.assertEqual(WebAppInfo("JFrog Artifactory Pro", "7.24.3"), result_artifactory)

        self.assertNotEqual(WebAppInfo("Atlassian Confluence", "88.5.7"), result_confluence)
        self.assertNotEqual(WebAppInfo("Atlassian Jira", "99.4.18"), result_jira)
        self.assertNotEqual(WebAppInfo("JFrog Artifactory Pro", "77.24.3"), result_artifactory)

        self.assertNotEqual(WebAppInfo("Atlassian Confluence", "8.5.7"), result_jira)
        self.assertNotEqual(WebAppInfo("Atlassian Jira", "9.4.18"), result_artifactory)
        self.assertNotEqual(WebAppInfo("JFrog Artifactory Pro", "7.24.3"), result_confluence)

    @patch.object(MockHtmlContentParsingMethod, '_get_web_app_rules', return_value=mock_web_app_rules)
    @patch.object(MockHtmlContentParsingMethod, '_get_full_page_content')
    def test_inspect_unknown_host(self, mock_get_full_page_content, mock_get_web_app_rules):
        mock_client = MagicMock(spec=IClientSideRenderer)
        detector = MockHtmlContentParsingMethod(client=mock_client)

        # Use the preloaded HTML content for the mock side effect
        mock_get_full_page_content.side_effect = lambda host: self.html_contents.get(host)

        result = detector.inspect_host('unknown.example.org')

        self.assertIsNone(result)
