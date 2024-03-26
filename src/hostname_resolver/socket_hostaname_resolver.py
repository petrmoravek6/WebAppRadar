from src.hostname_resolver.hostname_resolver import IHostnameResolver
import socket


class SocketHostnameResolver(IHostnameResolver):
    def resolve(self, ip: str) -> str:
        try:
            return socket.gethostbyname(ip)
        except socket.gaierror as e:  # todo
            print(f"Could not resolve hostname: {ip}")
            raise e
