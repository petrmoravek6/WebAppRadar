import uuid
from typing import Collection
from src.exceptions import FatalError
from src.hostname_info import HostnameInfo
from src.latest_version.full_info_fetcher import FullInfoFetcher
from src.scan_repository.scan_repository import IScanRepository
from src.vhost_net_scanner.vhost_net_scanner import IVhostNetScanner
from src.web_app_determiner.web_app_determiner import WebAppDeterminer
import logging

logger = logging.getLogger(__name__)


class WebAppRadar:
    """Class responsible for running complex scans that are capable of detecting web apps and compare them with current releases"""
    def __init__(self,
                 vhost_net_scanner: IVhostNetScanner,
                 web_app_determiner: WebAppDeterminer,
                 full_info_fetcher: FullInfoFetcher,
                 scan_repository: IScanRepository):
        self.vhost_net_scanner = vhost_net_scanner
        self.web_app_determiner = web_app_determiner
        self.full_info_fetcher = full_info_fetcher
        self.scan_repository = scan_repository

    def run(self, subnets: Collection[str], scan_id: str = str(uuid.uuid4())) -> Collection[HostnameInfo]:
        """
        Scans given subnets or IP addresses (or both) and returns a collection of web apps running in that network. The scan result is saved into database.
        :param subnets: subnets or IP addresses to be scanned
        :param scan_id: unique ID of the scan that is to be assigned to the database record
        :return: a collection of hostnames with running web apps. each element represents one hostname with running web app
        """
        logger.info(f"Scan (ID: {scan_id}) of: '{', '.join(subnets)}' started")
        status = 'success'
        res = []
        try:
            vhosts = self.vhost_net_scanner.get_all_vhosts(subnets)
            for vhost in vhosts:
                basic_info = self.web_app_determiner.detect_web_app_info(vhost)
                if basic_info is None:
                    res.append(HostnameInfo(hostname=vhost, full_web_app_info=None))
                else:
                    full_info = self.full_info_fetcher.get_full_info(basic_info)
                    res.append(HostnameInfo(hostname=vhost, full_web_app_info=full_info))
        except FatalError as fe:
            logger.error(f"Fatal error: {str(fe)}")
            logger.debug(f"Fatal error details: {fe.debug_msg}")
            status = 'fail'
        except Exception as e:
            logger.error(f"Unexpected error during running scan (ID: {scan_id}): {str(e)}")
            status = 'fail'
        finally:
            logger.info(f"Scan (ID: {scan_id}) of: '{subnets}' finished with status: '{status}'")
            self.scan_repository.create(scan_id, status, subnets, res)
            return res

    def get_scan_summaries(self):
        """
        Gets all historical scan summaries (ID, scan result, timestamp of completion)
        :return:
        """
        return self.scan_repository.get_all()

    def get_scan_details(self, scan_id):
        """
        Gets details of finished scan
        :param scan_id: ID of the scan
        :return: scan result details
        """
        return self.scan_repository.get_detail(scan_id)
