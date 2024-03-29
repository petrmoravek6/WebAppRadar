from src.hostname_resolver.hostname_resolver import IHostnameResolver
import socket


class SocketHostnameResolver(IHostnameResolver):
    def get_ip(self, hostname: str) -> str:
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror as e:
            raise ValueError(f"Invalid hostname. Could not get IP for: {hostname}")
