from abc import ABC
from src.ssh_client.ssh_client import ISSHClient, ShellOutput
from src.exceptions import FatalError


class ParamikoSSHClient(ISSHClient, ABC):
    def __init__(self, port: int = 22):
        """
        Initialize SSHClient with server details and authentication information.

        :param port: SSH port of the server
        """
        self.port = port
        self.connection = None

    def exec_command(self, command: str) -> ShellOutput:
        """Executes a command on the remote server."""
        if self.connection is None:
            raise FatalError("Fatal error in implementation logic",
                             "Connection not established. Call connect() first.")

        try:
            stdin, stdout, stderr = self.connection.exec_command(command)
            return ShellOutput(stdout.read().decode('utf-8'),
                               stderr.read().decode('utf-8'),
                               stdout.channel.recv_exit_status())
        except Exception as e:
            raise Exception(f"Failed to execute command: {command}. Error message: {e}")

    def close(self) -> None:
        """Closes the SSH connection."""
        if self.connection:
            self.connection.close()
        else:
            raise Exception("Connection was never established.")
