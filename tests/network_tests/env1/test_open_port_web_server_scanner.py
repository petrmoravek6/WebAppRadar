import unittest
from src.web_server_scanner.open_port_web_server_scanner import OpenPortWebServerScanner
from src.open_port_scanner.nmap_open_port_scanner import NMapOpenPortScanner


class TestOpenPortWebServerScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = OpenPortWebServerScanner(NMapOpenPortScanner())

    def test1(self):
        """Look for running 'nginx' and 'redis' hosts and 80 (nginx), 6379 (redis) and 22 (ssh - not present) ports"""
        result = self.scanner.discover(['nginx', 'redis'])

        expected = {'192.0.0.2'}

        self.assertEqual(result, expected)

    def test2(self):
        """Use IP addresses instead of hostnames"""
        result = self.scanner.discover(['192.0.0.2', '192.0.0.3'])

        expected = {'192.0.0.2'}

        self.assertCountEqual(result, expected)

    def test_non_existent_hosts(self):
        result = self.scanner.discover(['192.0.0.6', '192.0.0.7'])

        self.assertCountEqual(result, set())

    def test_whole_subnet(self):
        result = self.scanner.discover(['192.0.0.0/29'])

        self.assertTrue('192.0.0.2' in result)
        self.assertTrue('192.0.0.3' not in result)
        self.assertTrue('192.0.0.4' not in result)
        self.assertTrue('192.0.0.5' not in result)
        self.assertTrue('192.0.0.6' not in result)
        self.assertTrue('192.0.0.7' not in result)

    def test_mix_subnet_and_ips(self):
        result = self.scanner.discover(['192.0.0.0/29', '192.0.0.2', '192.0.0.3', '192.0.0.6'])

        self.assertTrue('192.0.0.2' in result)
        self.assertTrue('192.0.0.3' not in result)
        self.assertTrue('192.0.0.4' not in result)
        self.assertTrue('192.0.0.5' not in result)
        self.assertTrue('192.0.0.6' not in result)
        self.assertTrue('192.0.0.7' not in result)
