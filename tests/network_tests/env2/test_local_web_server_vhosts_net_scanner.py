import unittest
from src.open_port_scanner.nmap_open_port_scanner import NMapOpenPortScanner
from src.ssh_client.pwd_paramiko_ssh_client import PasswordParamikoSSHClient
from src.vhost_net_scanner.local_web_server_vhosts_net_scanner import LocalVhostsNetScanner
from src.web_server_scanner.open_port_web_server_scanner import OpenPortWebServerScanner
from src.vhost_discoverer.ssh_agent_vhost_discoverer import SshAgentVhostDiscoverer
from src.hostname_resolver.socket_hostaname_resolver import SocketHostnameResolver
from src.subnet_validator.pyt_hostname_subnet_validator import PytHostnameSubnetValidator
from src.subnet_validator.pyt_ip_subnet_validator import PytIPSubnetValidator
from src.vhosts_commands.apache2_vhosts_cmds import Apache2VhostsCmds
from src.vhosts_commands.nginx_vhosts_cmds import NginxVhostsCmds


class TestOpenPortWebServerScannerSystem(unittest.TestCase):
    """System/integration tests of the complete scan of network for its running web apps"""

    def setUp(self):
        hostname_resolver = SocketHostnameResolver()
        ip_validator = PytIPSubnetValidator()
        hostname_validator = PytHostnameSubnetValidator(hostname_resolver, ip_validator)

        ssh_pwd = 'test'
        ssh_user = 'test'
        web_server_cmds = (NginxVhostsCmds(), Apache2VhostsCmds())
        ssh_client = PasswordParamikoSSHClient(ssh_pwd)
        vhosts_discoverer = SshAgentVhostDiscoverer(ssh_client, web_server_cmds, ssh_user)

        open_port_scanner = NMapOpenPortScanner()
        web_server_scanner = OpenPortWebServerScanner(open_port_scanner)

        self.scanner = LocalVhostsNetScanner(web_server_scanner, vhosts_discoverer, hostname_validator)

    def test_ip_addresses(self):
        res1 = self.scanner.get_all_vhosts(('192.0.0.10', '192.0.0.11'))
        res2 = self.scanner.get_all_vhosts(('192.0.0.10',))
        res3 = self.scanner.get_all_vhosts(('192.0.0.11',))

        host1 = 'example1.mywebsite-webappradar.org'
        host2 = 'example2.mywebsite-webappradar.org'
        host3 = 'example3.mywebsite-webappradar.org'

        self.assertCountEqual(res1, (host1, host2, host3))
        self.assertCountEqual(res2, (host1,))
        self.assertCountEqual(res3, (host2, host3))

    def test_whole_subnet(self):
        res = self.scanner.get_all_vhosts(('192.0.0.8/29',))

        expected = ('example1.mywebsite-webappradar.org',
                    'example2.mywebsite-webappradar.org',
                    'example3.mywebsite-webappradar.org')

        self.assertCountEqual(res, expected)

    def test_edge_cases(self):
        empty_res = self.scanner.get_all_vhosts([])

        self.assertCountEqual(empty_res, [])
        self.assertRaises(ValueError, self.scanner.get_all_vhosts, ['das546546das'])
