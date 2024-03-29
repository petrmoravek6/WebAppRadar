import unittest
from src.open_port_scanner.nmap_open_port_scanner import NMapOpenPortScanner


class TestNMapOpenPortScanner(unittest.TestCase):

    def test_process_host_input_valid(self):
        input_hosts1 = ['192.168.1.1', '10.0.0.0/24', '192.168.60.0/24']
        expected_output1 = '192.168.1.1 10.0.0.0/24 192.168.60.0/24'
        input_hosts2 = ['10.0.0.0/24']
        expected_output2 = '10.0.0.0/24'
        input_hosts3 = ['192.168.22.22']
        expected_output3 = '192.168.22.22'

        result1 = NMapOpenPortScanner._process_host_input_for_nmap(input_hosts1)
        result2 = NMapOpenPortScanner._process_host_input_for_nmap(input_hosts2)
        result3 = NMapOpenPortScanner._process_host_input_for_nmap(input_hosts3)

        self.assertEqual(result1, expected_output1)
        self.assertEqual(result2, expected_output2)
        self.assertEqual(result3, expected_output3)

    def test_process_host_input_invalid(self):
        input_hosts = ['192.168.1.1', 'invalid_ip']
        with self.assertRaises(ValueError):
            NMapOpenPortScanner._process_host_input_for_nmap(input_hosts)

    def test_process_port_input_valid(self):
        input_ports1 = [80, 443]
        expected_output1 = '80,443'
        input_ports2 = [80, 443, 666]
        expected_output2 = '80,443,666'
        input_ports3 = [1000]
        expected_output3 = '1000'

        result1 = NMapOpenPortScanner._process_port_input_for_nmap(input_ports1)
        result2 = NMapOpenPortScanner._process_port_input_for_nmap(input_ports2)
        result3 = NMapOpenPortScanner._process_port_input_for_nmap(input_ports3)

        self.assertEqual(result1, expected_output1)
        self.assertEqual(result2, expected_output2)
        self.assertEqual(result3, expected_output3)

    def test_process_port_input_invalid(self):
        input_ports = [80, 7000000]  # 7000000 is out of the valid range
        with self.assertRaises(ValueError):
            NMapOpenPortScanner._process_port_input_for_nmap(input_ports)

    def test_process_host_input_empty(self):
        input_hosts = []
        expected_output = ''
        result = NMapOpenPortScanner._process_host_input_for_nmap(input_hosts)
        self.assertEqual(result, expected_output)

    def test_process_port_input_empty(self):
        input_ports = []
        expected_output = ''
        result = NMapOpenPortScanner._process_port_input_for_nmap(input_ports)
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
