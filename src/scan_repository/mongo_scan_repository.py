from datetime import datetime
from typing import Collection, Iterable
import logging
from pymongo import MongoClient
from src.scan_repository.scan_repository import IScanRepository
from src.hostname_info import HostnameInfo

logger = logging.getLogger(__name__)


class MongoScanRepository(IScanRepository):
    def __init__(self, connection_string: str):
        client = MongoClient(connection_string)
        self.db = client.web_app_radar

    @staticmethod
    def _get_hostname_info_as_api_dict(hostname_info: HostnameInfo):
        return {
            "hostname": hostname_info.hostname,
            "name": hostname_info.full_web_app_info.name if hostname_info.full_web_app_info else None,
            "version": hostname_info.full_web_app_info.version if hostname_info.full_web_app_info and hostname_info.full_web_app_info.version else None,
            "latest_version": hostname_info.full_web_app_info.latest_version if hostname_info.full_web_app_info and hostname_info.full_web_app_info.latest_version else None,
            "latest_cycle_version": hostname_info.full_web_app_info.latest_cycle_version if hostname_info.full_web_app_info and hostname_info.full_web_app_info.latest_cycle_version else None,
            "eol": hostname_info.full_web_app_info.eol if hostname_info.full_web_app_info and hostname_info.full_web_app_info.eol is not None else None,
            "eol_date": hostname_info.full_web_app_info.eol_date.isoformat() if hostname_info.full_web_app_info and hostname_info.full_web_app_info.eol_date else None
        }

    def get_all(self):
        try:
            results = list(self.db.results.find({}, {'_id': 1, 'completed_at': 1, 'status': 1}))
            # Sort the results by 'completed_at' field in ascending order
            results.sort(key=lambda r: r['completed_at'], reverse=True)
            return [{'id': str(result['_id']), 'completed_at': result['completed_at'], 'status': result['status']} for
                    result in results]
        except Exception as e:
            logger.error(f"Error during reading all scan summaries from DB, exception message: {str(e)}")
            return []

    def get_detail(self, _id: int):
        try:
            return self.db.results.find_one({'_id': _id})
        except Exception as e:
            logger.error(f"Error during reading a scan (ID: {_id}) result from DB, exception message: {str(e)}")
            return None

    def create(self, _id: str, status: str, subnets: Iterable[str], web_app_results: Collection[HostnameInfo]):
        try:
            result = {
                '_id': _id,
                'completed_at': datetime.now().isoformat(),
                'status': status,
                'subnets': ','.join(subnets),
                'web_apps': [MongoScanRepository._get_hostname_info_as_api_dict(info) for info in web_app_results]
            }
            self.db.results.insert_one(result)
        except Exception as e:
            logger.error(f"Error during saving a scan (ID: {_id}) result into DB, exception message: {str(e)}")
