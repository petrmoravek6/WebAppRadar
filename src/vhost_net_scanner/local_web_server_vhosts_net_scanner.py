from typing import Iterable

from src.subnet_validator.hostname_subnet_validator import IHostnameSubnetValidator
from src.vhost_discoverer.vhost_discoverer import IVhostDiscoverer
from src.vhost_net_scanner.web_server_vhost_net_scanner import WebServerVhostNetScanner
from src.web_server_scanner.web_server_scanner import IWebServerScanner


class LocalWebServerVhostsNetScanner(WebServerVhostNetScanner):
    def __init__(self,
                 web_server_scanner: IWebServerScanner,
                 vhost_discoverer: IVhostDiscoverer,
                 hostname_validator: IHostnameSubnetValidator):
        super().__init__(web_server_scanner, vhost_discoverer)
        self.hostname_validator = hostname_validator

    def get_all_vhosts(self, hosts: Iterable[str]) -> Iterable[str]:
        vhosts = super().get_all_vhosts(hosts)
        res = set()
        for vhost in vhosts:
            for host in hosts:
                if self.hostname_validator.is_hostname_in_subnet(vhost, host):
                    res.add(vhost)
                    break
        return res
            