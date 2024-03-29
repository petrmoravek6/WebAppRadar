from typing import Iterable
from src.ssh_client.ssh_client import ISSHClient
from src.vhost_discoverer.vhost_discoverer import IVhostDiscoverer
from src.vhosts_commands.vhosts_cmds import IVhostsCmds


class SshAgentVhostDiscoverer(IVhostDiscoverer):
    def __init__(self, ssh_client: ISSHClient, web_server_cmds: Iterable[IVhostsCmds], ssh_username: str):
        self.ssh_client = ssh_client
        self.web_server_cmds = web_server_cmds
        self.ssh_username = ssh_username

    def get_virtual_hosts(self, ip: str) -> Iterable[str]:
        self.ssh_client.connect(ip, self.ssh_username)
        res = set()
        for cmd in self.web_server_cmds:
            if self.ssh_client.exec_command(cmd.is_web_server_running()).exit_code == 0:
                server_vhosts_content = self.ssh_client.exec_command(cmd.get_content_from_server()).stdout
                vhosts = cmd.get_all_vhosts_from_content(server_vhosts_content)
                vhosts_w_localhost = {ip if (host == "localhost" or host == "127.0.0.1") else host for host in vhosts}
                res = res.union(vhosts_w_localhost)
        return res
