from src.hostname_resolver.hostname_resolver import IHostnameResolver
import socket


class SocketHostnameResolver(IHostnameResolver):
    def resolve_ip(self, hostname: str) -> str:
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror as e:  # todo
            print(f"Could not resolve hostname: {hostname}")
            raise e
