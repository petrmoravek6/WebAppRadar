import logging
import ipaddress
from threading import Lock
from src.web_app_radar import WebAppRadar

logger = logging.getLogger(__name__)


def validate_subnets(subnets):
    subnet_list = subnets.split(',')
    try:
        for subnet in subnet_list:
            ipaddress.ip_network(subnet, strict=False)
        return True
    except ValueError:
        return False


def run_scan(subnets: str, scan_id: str, scan_lock: Lock, web_app_radar: WebAppRadar):
    try:
        web_app_radar.run(subnets.split(','), scan_id)
    except Exception as e:
        logger.error(f"Unexpected error during running scan (ID: {scan_id}): {str(e)}")
    finally:
        scan_lock.release()
