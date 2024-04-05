import unittest
from src.vhost_discoverer.ssh_agent_vhost_discoverer import SshAgentVhostDiscoverer
from src.ssh_client.pwd_paramiko_ssh_client import PasswordParamikoSSHClient
from src.vhosts_commands.nginx_vhosts_cmds import NginxVhostsCmds
from src.vhosts_commands.apache2_vhosts_cmds import Apache2VhostsCmds


class TestParamikoSshAgentVhostDiscoverer(unittest.TestCase):
    """Integration tests for SshAgentVhostDiscoverer combined with ParamikoSSHClient (default SSH client) and apache + nginx vhosts commands"""
    def setUp(self):
        ssh_client_pwd = 'test'
        ssh_client_user = 'test'
        cmd1 = NginxVhostsCmds()
        cmd2 = Apache2VhostsCmds()
        ssh_client = PasswordParamikoSSHClient(ssh_client_pwd)
        self.discoverer = SshAgentVhostDiscoverer(ssh_client, (cmd1, cmd2,), ssh_client_user)

    def test_discover_vhosts(self):
        vhosts1 = self.discoverer.get_virtual_hosts('192.0.0.10')
        vhosts2 = self.discoverer.get_virtual_hosts('192.0.0.11')

        self.assertCountEqual(vhosts1, ('example1.mywebsite-webappradar.org',))
        self.assertCountEqual(vhosts2, ('example2.mywebsite-webappradar.org', 'example3.mywebsite-webappradar.org'))
