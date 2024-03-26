from src.open_port_scanner.nmap_open_port_scanner import NMapOpenPortScanner
from src.ssh_client.p_key_paramiko_ssh_client import PrivateKeyCipher
from src.ssh_client.p_key_paramiko_ssh_client import PrivateKeyParamikoSSHClient

sc = PrivateKeyParamikoSSHClient('192.168.68.130', 'moravekp', '/home/petr/.ssh/id_rsa_notiflight', PrivateKeyCipher.RSA)
sc.connect()
res = sc.exec_command('ls /')
sc.close()
print(res)