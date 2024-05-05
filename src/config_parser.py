import configparser
import os

from src.exceptions import FatalError
from src.ssh_client.p_key_paramiko_ssh_client import PrivateKeyCipher


class ConfigParser:
    def __init__(self, filename='config.ini'):
        self.config = configparser.ConfigParser()
        if not os.path.isfile(filename):
            raise FatalError(f"Config file at {filename} not found", "Use valid path to config file")
        self.config.read(filename)
        self._validate_config()

    def _validate_config(self):
        if 'SSH' in self.config:
            ssh_config = self.config['SSH']
            if 'method' in ssh_config:
                method = ssh_config['method']
                if method == 'private_key':
                    ConfigParser._validate_private_key(ssh_config)
                elif method == 'password':
                    ConfigParser._validate_password(ssh_config)
                else:
                    raise FatalError("Invalid SSH method in config file", "Use either 'private_key' or 'password' method")
            else:
                raise FatalError("Config file does not include 'method' in 'SSH' section")
        else:
            raise FatalError("Config file does not include 'SSH' section")

    @staticmethod
    def _validate_private_key(ssh_config):
        required_keys = ['path_to_private_key_file', 'private_key_cipher']
        for key in required_keys:
            if key not in ssh_config or not ssh_config[key]:
                raise FatalError(f"Missing or empty value for {key}")
        if not os.path.isfile(ssh_config['path_to_private_key_file']):
            raise FatalError(f"Private key file not found: {ssh_config['path_to_private_key_file']}")
        if ssh_config['private_key_cipher'] not in PrivateKeyCipher.__members__:
            raise FatalError(f"Invalid or not supported private key cipher: {ssh_config['private_key_cipher']}")

    @staticmethod
    def _validate_password(ssh_config):
        if 'password' not in ssh_config or not ssh_config['password']:
            raise FatalError(f"Missing or empty value for 'password' in config file")

    def get_ssh_config(self):
        if 'SSH' in self.config:
            return self.config['SSH']
        return None
