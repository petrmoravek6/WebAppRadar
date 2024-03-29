from src.open_port_scanner.nmap_open_port_scanner import NMapOpenPortScanner
from src.ssh_client.p_key_paramiko_ssh_client import PrivateKeyCipher
from src.ssh_client.p_key_paramiko_ssh_client import PrivateKeyParamikoSSHClient
from src.vhost_net_scanner.local_web_server_vhosts_net_scanner import LocalWebServerVhostsNetScanner
from src.web_server_scanner.open_port_web_server_scanner import OpenPortWebServerScanner
from src.vhost_discoverer.ssh_agent_vhost_discoverer import SshAgentVhostDiscoverer
from src.vhosts_commands.nginx_vhosts_cmds import NginxVhostsCmds
from src.hostname_resolver.socket_hostaname_resolver import SocketHostnameResolver
from src.subnet_validator.pyt_hostname_subnet_validator import PytHostnameSubnetValidator
from src.subnet_validator.pyt_ip_subnet_validator import PytIPSubnetValidator


nm = NMapOpenPortScanner()
ws_sc = OpenPortWebServerScanner(nm)

sc = PrivateKeyParamikoSSHClient('XXX', PrivateKeyCipher.RSA)
nginx_cmd = NginxVhostsCmds()
vhosts_dis = SshAgentVhostDiscoverer(sc, (nginx_cmd,), 'XXXX')

hnr = SocketHostnameResolver()
x = hnr.get_ip('192.168.68.119')
ip_subnet_validator = PytIPSubnetValidator()
hostname_subnet_validator = PytHostnameSubnetValidator(hnr, ip_subnet_validator)

f1 = LocalWebServerVhostsNetScanner(ws_sc, vhosts_dis, hostname_subnet_validator)
res = f1.get_all_vhosts(('192.168.68.140', '192.168.68.119'))
print(res)
