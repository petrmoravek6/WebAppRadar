from typing import Iterable

from src.vhost_net_scanner.vhost_net_scanner import IVhostNetScanner
from src.web_server_scanner.web_server_scanner import IWebServerScanner
from src.vhost_discoverer.vhost_discoverer import IVhostDiscoverer


class WebServerVhostNetScanner(IVhostNetScanner):
    def __init__(self, web_server_scanner: IWebServerScanner, vhost_discoverer: IVhostDiscoverer):
        super().__init__()
        self.web_server_scanner = web_server_scanner
        self.vhost_discoverer = vhost_discoverer

    def get_all_vhosts(self, hosts: Iterable[str]) -> Iterable[str]:
        res = set()
        ip_addresses = self.web_server_scanner.discover(hosts)
        for ip in ip_addresses:
            vhosts = self.vhost_discoverer.get_virtual_hosts(ip)
            res = res.union(set(vhosts))
        return res
