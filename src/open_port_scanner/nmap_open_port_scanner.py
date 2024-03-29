from nmap import PortScannerError
from src.open_port_scanner.open_port_scanner import IOpenPortScanner
from typing import Iterable, Dict
import nmap
import ipaddress
from src.exceptions import FatalError


class NMapOpenPortScanner(IOpenPortScanner):
    def __init__(self):
        super().__init__()
        self.nmap = nmap.PortScanner()

    @staticmethod
    def _process_host_input_for_nmap(hosts: Iterable[str]) -> str:
        validated_hosts = []
        for host in hosts:
            try:
                # This validation works for both IP addresses and subnets
                ipaddress.ip_network(host, strict=False)
                validated_hosts.append(host)
            except ValueError:
                raise ValueError(f"Invalid IP address or subnet: {host}")
        return ' '.join(validated_hosts)

    @staticmethod
    def _process_port_input_for_nmap(ports: Iterable[int]) -> str:
        validated_ports = []
        for port in ports:
            if 0 <= port <= 65535:
                validated_ports.append(str(port))
            else:
                raise ValueError(f"Invalid port number: {port}")
        return ','.join(validated_ports)

    def get_open_ports(self, hosts: Iterable[str], ports: Iterable[int]) -> Dict[str, Dict[str, bool]]:
        nmap_hosts = NMapOpenPortScanner._process_host_input_for_nmap(hosts)
        nmap_ports = NMapOpenPortScanner._process_port_input_for_nmap(ports)
        scan_results = {}
        try:
            # Launch the scan on the defined subnets and ports
            self.nmap.scan(hosts=nmap_hosts, arguments=f'-p {nmap_ports}')
        except PortScannerError:
            raise FatalError(f"Error during scanning {nmap_hosts} hosts. Unable to parse the scan output.",
                             "Nmap scan output was not XML. Exception thrown during using nmap's 'scan' method")

        # Loop through all the hosts found
        for host in self.nmap.all_hosts():
            # Check if the host status is up
            if self.nmap[host].state() == "up":
                # Initialize the host entry in the results dictionary
                scan_results[host] = {}

                # Loop through all protocols (tcp, udp) found for the host
                for proto in self.nmap[host].all_protocols():
                    # Get all scanned ports for the current protocol
                    lport = self.nmap[host][proto].keys()

                    for port in sorted(lport):
                        # Add port and its state (True for open, False otherwise) to the host's dictionary
                        scan_results[host][port] = self.nmap[host][proto][port]['state'] == 'open'
        return scan_results
