import unittest
from src.hostname_resolver.socket_hostaname_resolver import SocketHostnameResolver


class TestOpenPortWebServerScanner(unittest.TestCase):
    def setUp(self):
        self.resolver = SocketHostnameResolver()

    def test1(self):
        ip1 = self.resolver.get_ip('example1.mywebsite-webappradar.org')
        ip2 = self.resolver.get_ip('example2.mywebsite-webappradar.org')
        ip3 = self.resolver.get_ip('example3.mywebsite-webappradar.org')

        self.assertEqual(ip1, '192.0.0.10')
        self.assertEqual(ip2, '192.0.0.11')
        self.assertEqual(ip3, '192.0.0.11')

    def test2(self):
        """Use IP addresses instead of hostnames"""
        ip1 = self.resolver.get_ip('192.0.0.10')
        ip2 = self.resolver.get_ip('192.0.0.11')

        self.assertEqual(ip1, '192.0.0.10')
        self.assertEqual(ip2, '192.0.0.11')
