from src.subnet_validator.hostname_subnet_validator import IHostnameSubnetValidator
from src.subnet_validator.ip_subnet_validator import IIPSubnetValidator
from src.hostname_resolver.hostname_resolver import IHostnameResolver


class PytHostnameSubnetValidator(IHostnameSubnetValidator):
    def __init__(self, hostname_resolver: IHostnameResolver, ip_validator: IIPSubnetValidator):
        self.hostname_resolver = hostname_resolver
        self.ip_validator = ip_validator

    def is_hostname_in_subnet(self, hostname: str, subnet: str) -> bool:
        try:
            ip = self.hostname_resolver.resolve_ip(hostname)
            return self.ip_validator.is_ip_in_subnet(ip, subnet)
        except Exception:
            return False
