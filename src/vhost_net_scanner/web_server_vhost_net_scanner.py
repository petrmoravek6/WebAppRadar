import ipaddress
from typing import Iterable, Collection
import logging
from src.vhost_net_scanner.vhost_net_scanner import IVhostNetScanner
from src.web_server_scanner.web_server_scanner import IWebServerScanner
from src.vhost_discoverer.vhost_discoverer import IVhostDiscoverer

logger = logging.getLogger(__name__)


class WebServerVhostNetScanner(IVhostNetScanner):

    @staticmethod
    def _is_valid_ip_or_subnet(ip_or_subnet: str) -> bool:
        try:
            # Try to parse as an IP address
            ipaddress.ip_address(ip_or_subnet)
            return True
        except ValueError:
            pass  # Not a valid IP address
        try:
            # Try to parse as a subnet
            ipaddress.ip_network(ip_or_subnet, strict=False)
            return True
        except ValueError:
            pass  # Not a valid subnet

        return False

    def __init__(self, web_server_scanner: IWebServerScanner, vhost_discoverer: IVhostDiscoverer):
        super().__init__()
        self.web_server_scanner = web_server_scanner
        self.vhost_discoverer = vhost_discoverer

    def get_all_vhosts(self, subnets: Iterable[str]) -> Collection[str]:
        for subnet in subnets:
            if not self._is_valid_ip_or_subnet(subnet):
                raise ValueError(f"Invalid IP address or subnet: {subnet}")
        res = set()
        ip_addresses = self.web_server_scanner.discover(subnets)
        if not ip_addresses:
            logger.warning(f"No IP addresses found during web server scan of '{str(subnets)}'")
        for ip in ip_addresses:
            vhosts = self.vhost_discoverer.get_virtual_hosts(ip)
            if not vhosts:
                logger.warning(f"No virtual hosts found for server '{ip}' although the web server is probably running")
            res = res.union(set(vhosts))
        return res
