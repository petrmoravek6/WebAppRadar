import logging

from paramiko_ssh_client import ParamikoSSHClient
import paramiko


class PasswordParamikoSSHClient(ParamikoSSHClient):
    def __init__(self, password: str, port: int = 22):
        super().__init__(port)
        self.password = password

    def connect(self, host: str, user: str) -> None:
        """Establishes the SSH connection using a password."""
        try:
            self.connection = paramiko.SSHClient()
            self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.connection.connect(host, self.port, username=user, password=self.password)

            logging.debug(f"Connection established with host {host}:{self.port} using username: {user}")
        except Exception as e:
            self.connection = None
            raise ConnectionError(f"Failed to connect to host {host}:{self.port} using username: {user}. "
                                  f"Error message: {e}")
