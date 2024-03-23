from paramiko_ssh_client import ParamikoSSHClient
import paramiko


class PasswordParamikoSSHClient(ParamikoSSHClient):
    def __init__(self, ip: str, user: str, password: str, port: int = 22):
        super().__init__(ip, user, port)
        self.password = password

    def connect(self) -> None:
        """Establishes the SSH connection using a password."""
        try:
            self.connection = paramiko.SSHClient()
            self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.connection.connect(self.ip, self.port, username=self.user, password=self.password)

            print(f"Connection established with host {self.ip}:{self.port} using username: {self.user}")
        except Exception as e:
            self.connection = None
            raise ConnectionError(f"Failed to connect to host {self.ip}:{self.port} using username: {self.user}. "
                                  f"Error message: {e}")
