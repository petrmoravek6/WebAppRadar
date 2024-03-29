import unittest
from src.open_port_scanner.nmap_open_port_scanner import NMapOpenPortScanner


class TestOpenPortScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = NMapOpenPortScanner()

    def test1(self):
        """Look for running 'nginx' and 'redis' hosts and 80 (nginx), 6379 (redis) and 22 (ssh - not present) ports"""
        result = self.scanner.get_open_ports(['nginx', 'redis'], [80, 6379, 22])

        expected = {
            '192.0.0.2': {80: True, 6379: False, 22: False},
            '192.0.0.3': {80: False, 6379: True, 22: False}
        }
        self.assertEqual(result, expected)

    def test2(self):
        """Use IP addresses instead of hostnames"""
        result = self.scanner.get_open_ports(['192.0.0.2', '192.0.0.3'], [80, 6379, 22])

        expected = {
            '192.0.0.2': {80: True, 6379: False, 22: False},
            '192.0.0.3': {80: False, 6379: True, 22: False}
        }
        self.assertEqual(result, expected)
