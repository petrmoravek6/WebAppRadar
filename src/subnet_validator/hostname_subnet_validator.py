from src.subnet_validator.ihostname_subnet_validator import IHostnameSubnetValidator
from src.subnet_validator.iip_subnet_validator import IIPSubnetValidator
from src.hostname_resolver.hostname_resolver import IHostnameResolver
import logging

logger = logging.getLogger(__name__)


class HostnameSubnetValidator(IHostnameSubnetValidator):
    def __init__(self, hostname_resolver: IHostnameResolver, ip_validator: IIPSubnetValidator):
        self.hostname_resolver = hostname_resolver
        self.ip_validator = ip_validator

    def is_hostname_in_subnet(self, hostname: str, subnet: str) -> bool:
        try:
            ip = self.hostname_resolver.get_ip(hostname)
            return self.ip_validator.is_ip_in_subnet(ip, subnet)
        except Exception as e:
            logger.warning(f"Error during checking if hostname {hostname} was in subnet {subnet}. {e}")
            return False
