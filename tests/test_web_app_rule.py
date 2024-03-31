import unittest
import os
from src.web_app_determiner.web_app_rule import WebAppRule


class TestWebAppRule(unittest.TestCase):

    html_file_path1 = os.path.join(os.path.dirname(__file__), 'assets', 'jira-main-page.html')
    html_file_path2 = os.path.join(os.path.dirname(__file__), 'assets', 'not-jira-main-page.html')

    @classmethod
    def setUpClass(cls):
        super(TestWebAppRule, cls).setUpClass()
        # Assuming the HTML file is relatively located at 'tests/assets/jira-main-page.html'
        with open(cls.html_file_path1, 'r', encoding='utf-8') as f:
            cls.html_content1 = f.read()
        with open(cls.html_file_path2, 'r', encoding='utf-8') as f:
            cls.html_content2 = f.read()

    def test_matches(self):
        rule = WebAppRule(name="Atlassian Jira",
                          identifier=r'<meta name="application-name" content="JIRA" data-name="jira"',
                          version_path=None,
                          version=r'<meta name="application-name" content="JIRA" data-name="jira" data-version="(\d+\.\d+\.\d+)"')
        self.assertTrue(rule.matches(self.html_content1))

    def test_not_matches(self):
        rule1 = WebAppRule(name="Atlassian Jira",
                          identifier=r'<meta name="application-name" content="XX" data-name="XX"',
                          version_path=None,
                          version=r'<meta name="application-name" content="JIRA" data-name="jira" data-version="(\d+\.\d+\.\d+)"')
        rule2 = WebAppRule(name="Atlassian Jira",
                          identifier=r'<meta name="application-name" content="XX" data-name="XX"',
                          version_path=None,
                          version=r'<meta name="application-name" content="JIRA" data-name="jira" data-version="(\d+\.\d+\.\d+)"')
        self.assertFalse(rule1.matches(self.html_content1))
        self.assertFalse(rule2.matches(self.html_content2))

    def test_find_version(self):
        rule = WebAppRule(name="Atlassian Jira",
                          identifier=r'<meta name="application-name" content="JIRA" data-name="jira"',
                          version_path=None,
                          version=r'<meta name="application-name" content="JIRA" data-name="jira" data-version="(\d+\.\d+\.\d+)"')
        expected_version = "9.4.18"
        self.assertEqual(rule.find_version(self.html_content1), expected_version)
