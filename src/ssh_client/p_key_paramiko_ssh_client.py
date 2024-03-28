from src.ssh_client.paramiko_ssh_client import ParamikoSSHClient
import paramiko
from enum import Enum


class PrivateKeyCipher(Enum):
    RSA = 1
    ED25519 = 2
    ECDSA = 3
    DSS = 4


class PrivateKeyParamikoSSHClient(ParamikoSSHClient):
    key_class_map = {
        PrivateKeyCipher.RSA: paramiko.RSAKey,
        PrivateKeyCipher.ED25519: paramiko.Ed25519Key,
        PrivateKeyCipher.ECDSA: paramiko.ECDSAKey,
        PrivateKeyCipher.DSS: paramiko.DSSKey,
    }

    def __init__(self, private_key_path: str, private_key_cipher: PrivateKeyCipher, port: int = 22):
        super().__init__(port)
        self.private_key_path = private_key_path
        self.private_key_cipher = private_key_cipher

    def connect(self, ip: str, user: str) -> None:
        """Establishes the SSH connection using a private key."""
        try:
            self.connection = paramiko.SSHClient()
            self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.private_key_path and self.private_key_cipher in PrivateKeyParamikoSSHClient.key_class_map:
                key_class = PrivateKeyParamikoSSHClient.key_class_map[self.private_key_cipher]
                key = key_class.from_private_key_file(self.private_key_path)
                self.connection.connect(ip, self.port, username=user, pkey=key)
            elif self.private_key_path is None:
                raise ValueError("Private key path not provided.")
            else:
                raise ValueError("Unsupported private key cipher type.")

            print(f"Connection established with host {ip}:{self.port} using private key and username: {user}")
        except Exception as e:
            self.connection = None
            raise ConnectionError(f"Failed to connect to host {ip}:{self.port} using private key and username: "
                                  f"{user}. Error message: {e}")
