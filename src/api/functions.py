import logging
import ipaddress
from threading import Lock
from src.web_app_radar import WebAppRadar

logger = logging.getLogger(__name__)


def validate_subnets(subnets):
    subnet_list = subnets.split(',')
    for ip_or_subnet in subnet_list:
        try:
            # Try to parse as an IP address
            ipaddress.ip_address(ip_or_subnet)
            continue
        except ValueError:
            pass  # Not a valid IP address
        try:
            # Try to parse as a subnet
            ipaddress.ip_network(ip_or_subnet, strict=False)
            continue
        except ValueError:
            return False
    return True


def run_scan(subnets: str, scan_id: str, scan_lock: Lock, web_app_radar: WebAppRadar):
    try:
        web_app_radar.run(subnets.split(','), scan_id)
    except Exception as e:
        logger.error(f"Unexpected error during running scan (ID: {scan_id}): {str(e)}")
    finally:
        scan_lock.release()
