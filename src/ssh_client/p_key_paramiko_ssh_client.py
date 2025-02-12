from src.ssh_client.paramiko_ssh_client import ParamikoSSHClient
import paramiko
from enum import Enum
import logging
from src.exceptions import FatalError
logger = logging.getLogger(__name__)


class PrivateKeyParamikoSSHClient(ParamikoSSHClient):

    def __init__(self, private_key_path: str, port: int = 22):
        super().__init__(port)
        self.private_key_path = private_key_path

    def connect(self, host: str, user: str) -> None:
        """Establishes the SSH connection using a private key."""
        try:
            self.connection = paramiko.SSHClient()
            self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            self.connection.connect(host, self.port, username=user, key_filename=self.private_key_path)

            logger.debug(f"Connection established with host {host}:{self.port} using private key and username: {user}")
        except Exception as e:
            self.connection = None
            raise ConnectionError(f"Failed to connect to host {host}:{self.port} using private key and username: "
                                  f"{user}. Error message: {e}")
