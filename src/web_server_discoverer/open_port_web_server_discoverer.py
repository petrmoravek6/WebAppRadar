from typing import Iterable

from src.web_server_discoverer.web_server_discoverer import WebServerDiscoverer
from src.open_port_scanner.open_port_scanner import OpenPortScanner


class OpenPortWebServerDiscoverer(WebServerDiscoverer):
    web_server_ports = (80, 443)

    def __init__(self, open_port_scanner: OpenPortScanner):
        self.open_port_scanner = open_port_scanner

    def discover(self, hosts: Iterable[str]) -> Iterable[str]:
        ports_scan = self.open_port_scanner.get_open_ports(hosts, OpenPortWebServerDiscoverer.web_server_ports)
        return {key for key, port_list in ports_scan.items() if any(port_list.values())}
