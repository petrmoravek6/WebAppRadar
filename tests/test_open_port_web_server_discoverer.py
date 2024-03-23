import unittest
from unittest.mock import MagicMock
from src.web_server_discoverer.open_port_web_server_discoverer import OpenPortWebServerDiscoverer
from src.open_port_scanner.open_port_scanner import OpenPortScanner


class TestOpenPortWebServerDiscoverer(unittest.TestCase):
    def setUp(self):
        self.mock_scanner = MagicMock(spec=OpenPortScanner)
        self.discoverer = OpenPortWebServerDiscoverer(open_port_scanner=self.mock_scanner)

    def test_discover_with_open_web_servers(self):
        # Simulate open ports for specific hosts
        self.mock_scanner.get_open_ports.return_value = {
            '192.168.1.1': {'80': True, '443': False},
            '192.168.1.2': {'80': False, '443': True}
        }

        result = self.discoverer.discover(['192.168.1.1', '192.168.1.2'])
        self.assertEqual(set(result), {'192.168.1.1', '192.168.1.2'})

    def test_discover_with_no_open_web_servers(self):
        # Simulate no open web server ports
        self.mock_scanner.get_open_ports.return_value = {
            '192.168.1.1': {'80': False, '443': False},
            '192.168.1.2': {'80': False, '443': False}
        }

        result = self.discoverer.discover(['192.168.1.1', '192.168.1.2'])
        self.assertEqual(set(result), set())

    def test_discover_with_all_hosts_open(self):
        # Simulate all hosts have at least one open web server port
        self.mock_scanner.get_open_ports.return_value = {
            '10.0.0.1': {'80': True, '443': False},
            '10.0.0.2': {'80': False, '443': True},
            '10.0.0.3': {'80': True, '443': True}
        }

        result = self.discoverer.discover(['10.0.0.1', '10.0.0.2', '10.0.0.3'])
        self.assertEqual(set(result), {'10.0.0.1', '10.0.0.2', '10.0.0.3'})

    def test_discover_with_empty_input(self):
        # Test with no hosts provided
        self.mock_scanner.get_open_ports.return_value = {}

        result = self.discoverer.discover([])
        self.assertEqual(set(result), set())
