from typing import Iterable

from src.web_server_scanner.web_server_scanner import IWebServerScanner
from src.open_port_scanner.open_port_scanner import IOpenPortScanner


class OpenPortWebServerScanner(IWebServerScanner):
    web_server_ports = (80, 443)

    def __init__(self, open_port_scanner: IOpenPortScanner):
        self.open_port_scanner = open_port_scanner

    def discover(self, hosts: Iterable[str]) -> Iterable[str]:
        ports_scan = self.open_port_scanner.get_open_ports(hosts, OpenPortWebServerScanner.web_server_ports)
        return {key for key, port_list in ports_scan.items() if any(port_list.values())}
