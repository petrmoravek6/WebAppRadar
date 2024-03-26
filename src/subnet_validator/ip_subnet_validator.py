from src.subnet_validator.subnet_validator import ISubnetValidator
import ipaddress


class IPSubnetValidator(ISubnetValidator):
    def is_ip_in_subnet(self, ip_address: str, subnet: str) -> bool:
        # Convert the IP address and subnet to the appropriate objects
        ip_obj = ipaddress.ip_address(ip_address)
        subnet_obj = ipaddress.ip_network(subnet, strict=False)

        # Check if the IP address is within the subnet
        return ip_obj in subnet_obj
