import configparser
import os
from src.ssh_client.p_key_paramiko_ssh_client import PrivateKeyCipher


class ConfigParser:
    def __init__(self, filename='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.validate_config()

    def validate_config(self):
        # Validate SSH section
        if 'SSH' in self.config:
            ssh_config = self.config['SSH']
            if 'method' in ssh_config:
                method = ssh_config['method']
                if method == 'private_key':
                    ConfigParser._validate_private_key(ssh_config)

    @staticmethod
    def _validate_private_key(ssh_config):
        required_keys = ['path_to_private_key_file', 'private_key_cipher']
        for key in required_keys:
            if key not in ssh_config or not ssh_config[key]:
                raise ValueError(f"Missing or empty value for {key}")
        if not os.path.isfile(ssh_config['path_to_private_key_file']):
            raise FileNotFoundError(f"Private key file not found: {ssh_config['path_to_private_key_file']}")
        if ssh_config['private_key_cipher'] not in PrivateKeyCipher.__members__:
            raise ValueError(f"Invalid private key cipher: {ssh_config['private_key_cipher']}")

    def get_ssh_config(self):
        if 'SSH' in self.config:
            return self.config['SSH']
        return None
