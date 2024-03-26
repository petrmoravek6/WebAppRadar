import unittest
from src.subnet_validator.pyt_ip_subnet_validator import PytIPSubnetValidator


class TestIPSubnetValidator(unittest.TestCase):

    def setUp(self):
        self.validator = PytIPSubnetValidator()

    def test_ip_in_subnet(self):
        # Standard case within subnet
        self.assertTrue(self.validator.is_ip_in_subnet("192.168.1.10", "192.168.1.0/24"))
        self.assertTrue(self.validator.is_ip_in_subnet("192.168.1.10", "192.168.1.10"))
        self.assertTrue(self.validator.is_ip_in_subnet("10.0.0.1", "10.0.0.0/8"))
        # Edge case: First IP in the range
        self.assertTrue(self.validator.is_ip_in_subnet("192.168.1.1", "192.168.1.0/24"))
        # Edge case: Last IP in the range
        self.assertTrue(self.validator.is_ip_in_subnet("192.168.1.254", "192.168.1.0/24"))

    def test_ip_not_in_subnet(self):
        # IP outside of subnet range
        self.assertFalse(self.validator.is_ip_in_subnet("192.168.2.10", "192.168.1.0/24"))
        self.assertFalse(self.validator.is_ip_in_subnet("192.168.1.10", "192.168.1.111"))
        # Completely different subnet
        self.assertFalse(self.validator.is_ip_in_subnet("10.0.0.1", "192.168.1.0/24"))
        # Border case: IP just outside the subnet
        self.assertFalse(self.validator.is_ip_in_subnet("192.168.0.255", "192.168.1.0/24"))
        self.assertFalse(self.validator.is_ip_in_subnet("192.168.2.0", "192.168.1.0/24"))

    def test_edge_case_network_address(self):
        self.assertTrue(self.validator.is_ip_in_subnet("192.168.1.0", "192.168.1.0/24"))

    def test_edge_case_broadcast_address(self):
        self.assertTrue(self.validator.is_ip_in_subnet("192.168.1.255", "192.168.1.0/24"))

    def test_ip_v6_in_subnet(self):
        self.assertTrue(self.validator.is_ip_in_subnet("2001:db8::1", "2001:db8::/32"))

    def test_ip_v6_not_in_subnet(self):
        self.assertFalse(self.validator.is_ip_in_subnet("2001:db8::1", "2001:db9::/32"))

    def test_invalid_ip_address(self):
        with self.assertRaises(ValueError):
            self.validator.is_ip_in_subnet("invalid_ip", "192.168.1.0/24")

    def test_invalid_subnet(self):
        with self.assertRaises(ValueError):
            self.validator.is_ip_in_subnet("192.168.1.10", "invalid_subnet")
