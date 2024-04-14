from typing import Collection, NamedTuple, Optional
from src.latest_version.full_info_fetcher import FullInfoFetcher
from src.vhost_net_scanner.vhost_net_scanner import IVhostNetScanner
from src.web_app_determiner.web_app_determiner import WebAppDeterminer
from src.latest_version.full_web_app_info import FullWebAppInfo


class HostnameInfo(NamedTuple):
    hostname: str
    full_web_app_info: Optional[FullWebAppInfo]


class WebAppRadar:
    def __init__(self,
                 vhost_net_scanner: IVhostNetScanner,
                 web_app_determiner: WebAppDeterminer,
                 full_info_fetcher: FullInfoFetcher):
        self.vhost_net_scanner = vhost_net_scanner
        self.web_app_determiner = web_app_determiner
        self.full_info_fetcher = full_info_fetcher

    def run(self, subnets: Collection[str]) -> Collection[HostnameInfo]:
        vhosts = self.vhost_net_scanner.get_all_vhosts(subnets)
        res = []
        for vhost in vhosts:
            basic_info = self.web_app_determiner.detect_web_app_info(vhost)
            if basic_info is None:
                res.append(HostnameInfo(hostname=vhost, full_web_app_info=None))
            else:
                full_info = self.full_info_fetcher.fetch(basic_info)
                res.append(HostnameInfo(hostname=vhost, full_web_app_info=full_info))
        return res
