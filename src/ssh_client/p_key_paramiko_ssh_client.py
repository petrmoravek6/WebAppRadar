from paramiko_ssh_client import ParamikoSSHClient
import paramiko


class PrivateKeyParamikoSSHClient(ParamikoSSHClient):
    def __init__(self, private_key_path: str, ip: str, user: str, port: int = 22):
        super().__init__(ip, user, port)
        self.private_key_path = private_key_path

    def connect(self) -> None:
        """Establishes the SSH connection using either a private key or password."""
        try:
            self.connection = paramiko.SSHClient()
            self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.private_key_path:
                key = paramiko.RSAKey.from_private_key_file(self.private_key_path)
                self.connection.connect(self.ip, self.port, username=self.user, pkey=key)

            print(f"Connection established with host {self.ip}:{self.port} using private key and username: {self.user}")
        except Exception as e:
            self.connection = None
            raise ConnectionError(f"Failed to connect to host {self.ip}:{self.port} using private key and username: "
                                  f"{self.user}. Error message: {e}")
