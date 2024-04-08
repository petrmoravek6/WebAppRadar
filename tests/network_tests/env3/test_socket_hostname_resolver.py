import unittest
from src.hostname_resolver.socket_hostaname_resolver import SocketHostnameResolver


class TestSocketHostnameResolver(unittest.TestCase):
    def setUp(self):
        self.resolver = SocketHostnameResolver()

    def test_get_ip_valid_hostnames(self):
        expected_ips = {
            "jira.webappradar-example.io": "192.0.0.18",
            "grafana.webappradar-example.io": "192.0.0.21",
            "bareos.webappradar-example.io": "192.0.0.21",
            "keycloak.webappradar-example.io": "192.0.0.21",
            "gitlab.webappradar-example.io": "192.0.0.19",
            "prometheus.webappradar-example.io": "192.0.0.19",
            "snipe-it.webappradar-example.io": "192.0.0.19",
            "teamcity.webappradar-example.io": "192.0.0.19",
            "testrail.webappradar-example.io": "192.0.0.19",
        }

        for hostname, expected_ip in expected_ips.items():
            with self.subTest(hostname=hostname):
                ip = self.resolver.get_ip(hostname)
                self.assertEqual(ip, expected_ip, f"Failed for hostname: {hostname}")

    def test_get_ip_invalid_hostname(self):
        with self.assertRaises(ValueError):
            self.resolver.get_ip("invalid.hostname.example.465465")
