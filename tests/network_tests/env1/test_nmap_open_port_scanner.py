import unittest
from src.open_port_scanner.nmap_open_port_scanner import NMapOpenPortScanner


class TestNMapOpenPortScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = NMapOpenPortScanner()

    def test1(self):
        """Look for running 'nginx' and 'redis' hosts and 80 (nginx), 6379 (redis) and 22 (ssh - not present) ports"""
        result = self.scanner.get_open_ports(['nginx', 'redis'], [80, 6379, 22])

        expected = {
            '192.0.0.2': {80: True, 6379: False, 22: False},
            '192.0.0.3': {80: False, 6379: True, 22: False}
        }
        self.assertDictEqual(result, expected)

    def test2(self):
        """Use IP addresses instead of hostnames"""
        result = self.scanner.get_open_ports(['192.0.0.2', '192.0.0.3'], [80, 6379, 22])

        expected = {
            '192.0.0.2': {80: True, 6379: False, 22: False},
            '192.0.0.3': {80: False, 6379: True, 22: False}
        }
        self.assertDictEqual(result, expected)

    def test_non_existent_hosts(self):
        result = self.scanner.get_open_ports(['192.0.0.6', '192.0.0.7'], [80, 6379, 22])

        expected = dict()
        self.assertDictEqual(result, expected)

    def test_whole_subnet(self):
        result = self.scanner.get_open_ports(['192.0.0.0/29'], [80, 6379, 22])

        nginx_res = {80: True, 6379: False, 22: False}
        redis_res = {80: False, 6379: True, 22: False}

        self.assertDictEqual(result['192.0.0.2'], nginx_res)
        self.assertDictEqual(result['192.0.0.3'], redis_res)
        # no host present in the subnet other than the app, nginx, redis and default gateway
        self.assertEqual(result.keys(), {'192.0.0.1', '192.0.0.2', '192.0.0.3', '192.0.0.4'})

    def test_mix_subnet_and_ips(self):
        result = self.scanner.get_open_ports(['192.0.0.0/29', '192.0.0.2', '192.0.0.3', '192.0.0.6'], [80, 6379, 22])

        nginx_res = {80: True, 6379: False, 22: False}
        redis_res = {80: False, 6379: True, 22: False}

        self.assertDictEqual(result['192.0.0.2'], nginx_res)
        self.assertDictEqual(result['192.0.0.3'], redis_res)
        # no host present in the subnet other than the app, nginx, redis and default gateway
        self.assertEqual(result.keys(), {'192.0.0.1', '192.0.0.2', '192.0.0.3', '192.0.0.4'})
