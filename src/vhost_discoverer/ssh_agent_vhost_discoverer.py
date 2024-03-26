from typing import Iterable
from src.ssh_client.ssh_client import ISSHClient
from src.vhost_discoverer.vhost_discoverer import IVhostDiscoverer
from src.vhosts_command.vhosts_cmd import IVhostsCmd


class SshAgentVhostDiscoverer(IVhostDiscoverer):
    def __init__(self, ssh_client: ISSHClient, web_server_cmds: Iterable[IVhostsCmd]):
        self.ssh_client = ssh_client
        self.web_server_cmds = web_server_cmds

    def get_virtual_hosts(self, ip: str) -> Iterable[str]:
        self.ssh_client.connect()
        res = set()
        for cmd in self.web_server_cmds:
            if self.ssh_client.exec_command(cmd.is_web_server_running()).exit_code == 0:
                curr_vhosts = self.ssh_client.exec_command(cmd.get_all_vhosts()).stdout.splitlines()
                res.union(set(curr_vhosts))
        return res
