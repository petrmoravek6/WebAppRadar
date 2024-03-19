from src.open_port_scanner.nmap_open_port_scanner import NMapOpenPortScanner

sc = NMapOpenPortScanner()
# res = sc.get_open_ports(('192.168.74.56', '192.168.74.60', '192.168.74.66'), (80, 443))
res = sc.get_open_ports(('192.168.74.101',), (80, 443))
print(res)

import paramiko

connection = paramiko.SSHClient()
connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
connection.connect()