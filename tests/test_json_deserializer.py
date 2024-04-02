import unittest

from src.web_app_determiner.web_app_rule.authentication.html_elem_param import HTMLElementParam
from src.web_app_determiner.web_app_rule.authentication.user_and_pwd_auth import UserAndPwdAuth
from src.web_app_determiner.web_app_rule.json_deserializer import JsonWebAppRulesDeserializer


class TestJsonWebAppRulesDeserializer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.deserializer = JsonWebAppRulesDeserializer()
        cls.rules = cls.deserializer.deserialize(cls._load_file('tests/assets/web-apps.json'))

    @classmethod
    def _load_file(cls, file_name):
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.read()

    def find_rule_by_name(self, name):
        """Utility method to find a WebAppRule by its name."""
        return next((rule for rule in self.rules if rule.name == name), None)

    def test_deserialize_count(self):
        """Test the correct number of WebAppRule objects are created."""
        self.assertEqual(len(self.rules), 13)

    def test_deserialize_auth_for_gitlab(self):
        """Test that GitLab auth objects are correctly created."""
        gitlab_rule = self.find_rule_by_name("GitLab")
        expected_user_params = [HTMLElementParam("name", "username")]
        expected_pwd_params = [HTMLElementParam("name", "password")]
        expected_method = "username_and_password"

        self.assertIsNotNone(gitlab_rule)
        self.assertIsInstance(gitlab_rule.auth, UserAndPwdAuth)
        self.assertEqual(gitlab_rule.auth.method, expected_method)
        self.assertIsNotNone(gitlab_rule.auth)
        self.assertEqual(gitlab_rule.auth.user_box_params, expected_user_params)
        self.assertEqual(gitlab_rule.auth.pwd_box_params, expected_pwd_params)

    def test_deserialize_without_auth_for_jira(self):
        """Test deserialization of WebAppRules without auth details for Jira."""
        jira_rule = self.find_rule_by_name("Atlassian Jira")
        self.assertIsNotNone(jira_rule)
        self.assertIsNone(jira_rule.auth)

    def test_deserialize_version_path_for_prometheus(self):
        """Test correct deserialization of version_path for Prometheus."""
        prometheus_rule = self.find_rule_by_name("Prometheus")
        self.assertIsNotNone(prometheus_rule)
        self.assertEqual(prometheus_rule.version_path, "/status")

    def test_zabbix_auth_params(self):
        """Test the user_box_params and pwd_box_params of Zabbix's Auth object."""
        zabbix_rule = self.find_rule_by_name("Zabbix")
        expected_user_params = [HTMLElementParam("id", "name")]
        expected_pwd_params = [HTMLElementParam("id", "password")]

        self.assertIsNotNone(zabbix_rule.auth)
        self.assertIsNotNone(zabbix_rule.auth, UserAndPwdAuth)
        self.assertEqual(zabbix_rule.auth.user_box_params, expected_user_params)
        self.assertEqual(zabbix_rule.auth.pwd_box_params, expected_pwd_params)

    def test_auth_path_for_keycloak(self):
        """Test the auth_path of Keycloak's Auth object."""
        keycloak_rule = self.find_rule_by_name("Keycloak")
        self.assertIsNotNone(keycloak_rule.auth)
        self.assertEqual(keycloak_rule.auth.auth_path, "/admin/master/console/")

    def test_auth_method_types(self):
        """Test that the auth method is correctly identified as UserAndPwdAuth."""
        expected_username = "user123"
        expected_pwd = "password123"
        for rule_name in ["GitLab", "Zabbix", "Graylog", "Snipe-IT", "Keycloak"]:
            rule = self.find_rule_by_name(rule_name)
            self.assertIsNotNone(rule.auth, f"{rule_name} should have an auth object.")
            self.assertIsInstance(rule.auth, UserAndPwdAuth, f"{rule_name}'s auth should be UserAndPwdAuth.")
            self.assertEqual(rule.auth.username, expected_username)
            self.assertEqual(rule.auth.password, expected_pwd)

    def test_auth_object_completeness(self):
        """Test for completeness of the Auth object for a given application."""
        # Example for Keycloak
        keycloak_rule = self.find_rule_by_name("Keycloak")
        self.assertIsNotNone(keycloak_rule.auth)
        self.assertEqual(keycloak_rule.auth.method, "username_and_password")
        self.assertTrue(len(keycloak_rule.auth.user_box_params) > 0, "User box params should not be empty.")
        self.assertTrue(len(keycloak_rule.auth.pwd_box_params) > 0, "Password box params should not be empty.")
