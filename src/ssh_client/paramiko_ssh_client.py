from abc import ABC
from typing import Tuple

from ssh_client import SSHClient


class ParamikoSSHClient(SSHClient, ABC):
    def __init__(self, ip: str, user: str, port: int = 22):
        """
        Initialize SSHClient with server details and authentication information.

        :param ip: IP address of the server
        :param user: Username for authentication
        :param port: SSH port of the server
        """
        self.ip = ip
        self.port = port
        self.user = user
        self.connection = None

    def exec_command(self, command: str) -> Tuple[str, str]:
        """Executes a command on the remote server."""
        if self.connection is None:
            raise Exception("Connection not established. Call connect() first.")

        try:
            stdin, stdout, stderr = self.connection.exec_command(command)
            return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')
        except Exception as e:
            raise Exception(f"Failed to execute command. Error message: {e}")

    def close(self) -> None:
        """Closes the SSH connection."""
        if self.connection:
            self.connection.close()
        else:
            raise Exception("Connection was never established.")
