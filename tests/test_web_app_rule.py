import unittest
import os

from src.web_app_determiner.web_app_rule.authentication.html_elem_param import HTMLElementParam
from src.web_app_determiner.web_app_rule.authentication.user_and_pwd_auth import UserAndPwdAuth
from src.web_app_determiner.web_app_rule.web_app_rule import WebAppRule


class TestWebAppRule(unittest.TestCase):
    html_file_path1 = os.path.join(os.path.dirname(__file__), 'assets', 'jira-main-page.html')
    html_file_path2 = os.path.join(os.path.dirname(__file__), 'assets', 'not-jira-main-page.html')
    html_file_path3 = os.path.join(os.path.dirname(__file__), 'assets', 'keycloak-main-page.html')
    html_file_path4 = os.path.join(os.path.dirname(__file__), 'assets', 'keycloak-aa.html')

    @classmethod
    def load_file(cls, path: str) -> str:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @classmethod
    def setUpClass(cls):
        super(TestWebAppRule, cls).setUpClass()
        cls.html_content1 = cls.load_file(cls.html_file_path1)
        cls.html_content2 = cls.load_file(cls.html_file_path2)
        cls.html_content3 = cls.load_file(cls.html_file_path3)
        cls.html_content4 = cls.load_file(cls.html_file_path4)

    def test_matches(self):
        rule1 = WebAppRule(web_app_name="Atlassian Jira",
                           identifier=r'<meta name="application-name" content="JIRA" data-name="jira"',
                           version_string=r'<meta name="application-name" content="JIRA" data-name="jira" data-version="(\d+\.\d+\.\d+)"')
        rule2 = WebAppRule(web_app_name="Keycloak",
                           identifier='<title>Welcome to Keycloak</title>',
                           version_string="<div class=\"pf-c-description-list__text\">(\\d+\\.\\d+\\.\\d+)</div>",
                           auth=UserAndPwdAuth(
                               method="username_and_password",
                               user_box_params=[HTMLElementParam(key="key", value="value")],
                               pwd_box_params=[HTMLElementParam(key="key", value="value")],
                               username="XXX",
                               password="XXX"
                           ))
        self.assertTrue(rule1.matches(self.html_content1))
        self.assertTrue(rule2.matches(self.html_content3))

    def test_not_matches(self):
        rule1 = WebAppRule(web_app_name="Atlassian Jira",
                           identifier=r'<meta name="application-name" content="XX" data-name="XX"',
                           version_string=r'<meta name="application-name" content="JIRA" data-name="jira" data-version="(\d+\.\d+\.\d+)"')
        rule2 = WebAppRule(web_app_name="Atlassian Jira",
                           identifier=r'<meta name="application-name" content="XX" data-name="XX"',
                           version_string=r'<meta name="application-name" content="JIRA" data-name="jira" data-version="(\d+\.\d+\.\d+)"')
        self.assertFalse(rule1.matches(self.html_content1))
        self.assertFalse(rule2.matches(self.html_content2))

    def test_find_version(self):
        rule = WebAppRule(web_app_name="Atlassian Jira",
                          identifier=r'<meta name="application-name" content="JIRA" data-name="jira"',
                          version_string=r'<meta name="application-name" content="JIRA" data-name="jira" data-version="(\d+\.\d+\.\d+)"')
        rule2 = WebAppRule(web_app_name="Keycloak",
                           identifier='<title>Welcome to Keycloak</title>',
                           version_string="<div class=\"pf-c-description-list__text\">(\\d+\\.\\d+\\.\\d+)</div>",
                           auth=UserAndPwdAuth(
                               method="username_and_password",
                               user_box_params=[HTMLElementParam(key="key", value="value")],
                               pwd_box_params=[HTMLElementParam(key="key", value="value")],
                               username="XXX",
                               password="XXX"
                           ))
        expected_version = "9.4.18"
        expected_version2 = "22.0.3"
        self.assertEqual(rule.find_version(self.html_content1), expected_version)
        self.assertEqual(rule2.find_version(self.html_content4), expected_version2)
