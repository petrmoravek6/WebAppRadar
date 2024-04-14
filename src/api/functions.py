import os
import time
from pymongo import MongoClient
from src.exceptions import FatalError
from src.web_app_radar import WebAppRadar, HostnameInfo
import logging
from threading import Lock
import datetime
import ipaddress

SCAN_LOCK = Lock()
logger = logging.getLogger(__name__)


def init_db_connection():
    mongo_connection_str = os.getenv('MONGO_URI')
    if not mongo_connection_str:
        raise Exception("MONGO_URI env (connection string for MongoDB) not defined")
    client = MongoClient(mongo_connection_str)
    return client.webapp_radar


def validate_subnets(subnets):
    subnet_list = subnets.split(',')
    try:
        for subnet in subnet_list:
            ipaddress.ip_network(subnet, strict=False)
        return True
    except ValueError:
        return False


def hostname_info_as_api_dict(hostname_info: HostnameInfo):
    return {
        "hostname": hostname_info.hostname,
        "name": hostname_info.full_web_app_info.name if hostname_info.full_web_app_info else None,
        "version": hostname_info.full_web_app_info.version if hostname_info.full_web_app_info and hostname_info.full_web_app_info.version else None,
        "latest_version": hostname_info.full_web_app_info.latest_version if hostname_info.full_web_app_info and hostname_info.full_web_app_info.latest_version else None,
        "latest_cycle_version": hostname_info.full_web_app_info.latest_cycle_version if hostname_info.full_web_app_info and hostname_info.full_web_app_info.latest_cycle_version else None,
        "eol": hostname_info.full_web_app_info.eol if hostname_info.full_web_app_info and hostname_info.full_web_app_info.eol is not None else None,
        "eol_date": hostname_info.full_web_app_info.eol_date.isoformat() if hostname_info.full_web_app_info and hostname_info.full_web_app_info.eol_date else None
    }


def run_scan(subnets: str, scan_id: str, scan_loc: Lock, db_client, web_app_radar: WebAppRadar = None):
    scan_loc.acquire()
    try:
        status = 'success'
        scan_results = tuple()
        try:
            scan_results = web_app_radar.run(subnets.split(','))
            # scan_results = [
            #     HostnameInfo('192.168.120.100', FullWebAppInfo('Jira', '5', '7', '6', eol=False, eol_date=datetime.date.today())),
            #     HostnameInfo('192.168.120.101', FullWebAppInfo('Confluence', '8', '9', '8.2')),
            #     HostnameInfo('192.168.120.102', FullWebAppInfo('Bareos', '6', '7')),
            #     HostnameInfo('192.168.120.103', FullWebAppInfo('Git', '6')),
            #     HostnameInfo('192.168.120.104', FullWebAppInfo('Test')),
            #     HostnameInfo('192.168.120.105', None),
            # ]
            # time.sleep(20)
        except FatalError as fe:
            logger.error(f"Fatal error: {str(fe)}")
            logger.debug(f"Fatal error details: {fe.debug_msg}")
            status = 'fail'
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            status = 'fail'

        result = {
            '_id': scan_id,
            'completed_at': datetime.datetime.now().isoformat(),
            'status': status,
            'subnets': subnets,
            'web_apps': [hostname_info_as_api_dict(info) for info in scan_results]
        }

        # Insert the document into MongoDB
        db_client.results.insert_one(result)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        scan_loc.release()
