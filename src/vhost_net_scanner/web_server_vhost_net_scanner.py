from typing import Iterable
import logging
from src.vhost_net_scanner.vhost_net_scanner import IVhostNetScanner
from src.web_server_scanner.web_server_scanner import IWebServerScanner
from src.vhost_discoverer.vhost_discoverer import IVhostDiscoverer

logger = logging.getLogger(__name__)


class WebServerVhostNetScanner(IVhostNetScanner):
    def __init__(self, web_server_scanner: IWebServerScanner, vhost_discoverer: IVhostDiscoverer):
        super().__init__()
        self.web_server_scanner = web_server_scanner
        self.vhost_discoverer = vhost_discoverer

    def get_all_vhosts(self, hosts: Iterable[str]) -> Iterable[str]:
        res = set()
        ip_addresses = self.web_server_scanner.discover(hosts)
        if len(ip_addresses) < 1:
            logger.warning(f"No IP addresses found during web server scan of '{hosts}'")
        for ip in ip_addresses:
            vhosts = self.vhost_discoverer.get_virtual_hosts(ip)
            if len(vhosts) < 1:
                logger.warning(f"No virtual hosts found for server '{ip}' although the web server is probably running")
            res = res.union(set(vhosts))
        return res
