from typing import Iterable
from src.ssh_client.ssh_client import ISSHClient
from src.vhost_discoverer.vhost_discoverer import IVhostDiscoverer
from src.vhosts_commands.vhosts_cmds import IVhostsCmds
import logging

logger = logging.getLogger(__name__)


class SshAgentVhostDiscoverer(IVhostDiscoverer):
    def __init__(self, ssh_client: ISSHClient, web_server_cmds: Iterable[IVhostsCmds], ssh_username: str):
        self.ssh_client = ssh_client
        self.web_server_cmds = web_server_cmds
        self.ssh_username = ssh_username

    def get_virtual_hosts(self, host: str) -> Iterable[str]:
        try:
            self.ssh_client.connect(host, self.ssh_username)
        except ConnectionError as e:
            logger.error(e)
            return []
        res = set()
        for cmd in self.web_server_cmds:
            try:
                cmd1 = self.ssh_client.exec_command(cmd.is_web_server_running())
                if cmd1.exit_code == 0:
                    logger.debug(f"Web server detected on '{host}' using '{cmd.is_web_server_running()}' command to "
                                 f"check zero exit code")
                    server_vhosts_content = self.ssh_client.exec_command(cmd.get_content_from_server()).stdout
                    vhosts = cmd.get_all_vhosts_from_content(server_vhosts_content)
                    vhosts_w_localhost = {host if (vhost == "localhost" or vhost == "127.0.0.1") else vhost for vhost in
                                          vhosts}
                    res = res.union(vhosts_w_localhost)
                else:
                    logger.debug(f"Could not check if web server is running using '{cmd.is_web_server_running()}' on "
                                 f"'{host}' exit code: {cmd1.exit_code}, stdout: {cmd1.stdout}, stderr: {cmd1.stdout}"
                                 f", stderr: {cmd1.stderr}")
            except Exception as e:
                logger.error(f"Error during SSH {host} inspection. {e}")
                return res
        return res
