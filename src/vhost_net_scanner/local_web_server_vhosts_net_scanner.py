from typing import Iterable, Collection
from src.subnet_validator.hostname_subnet_validator import IHostnameSubnetValidator
from src.vhost_discoverer.vhost_discoverer import IVhostDiscoverer
from src.vhost_net_scanner.web_server_vhost_net_scanner import WebServerVhostNetScanner
from src.web_server_scanner.web_server_scanner import IWebServerScanner


class LocalWebServerVhostNetScanner(WebServerVhostNetScanner):
    def __init__(self,
                 web_server_scanner: IWebServerScanner,
                 vhost_discoverer: IVhostDiscoverer,
                 hostname_validator: IHostnameSubnetValidator):
        super().__init__(web_server_scanner, vhost_discoverer)
        self.hostname_validator = hostname_validator

    def get_all_vhosts(self, subnets: Iterable[str]) -> Collection[str]:
        vhosts = super().get_all_vhosts(subnets)
        res = set()
        for vhost in vhosts:
            for subnet in subnets:
                if self.hostname_validator.is_hostname_in_subnet(vhost, subnet):
                    res.add(vhost)
                    break
        return res
            