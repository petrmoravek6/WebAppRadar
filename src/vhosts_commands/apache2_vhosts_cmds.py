from src.vhosts_commands.vhosts_cmds import IVhostsCmds
import re


class Apache2VhostsCmds(IVhostsCmds):
    def is_web_server_running(self) -> str:
        return ("systemctl -q is-active apache2 || (service apache2 status > /dev/null 2>&1 && service apache2 status "
                "| grep -q 'active (running)')")

    def get_content_from_server(self) -> str:
        return "cat /etc/apache2/sites-enabled/*"

    def get_all_vhosts_from_content(self, content: str) -> set[str]:
        virtualhost_blocks = re.findall(r'<VirtualHost.*?>(.*?)</VirtualHost>', content, re.DOTALL)

        # Using a set to store server names to ensure uniqueness
        server_names = set()
        for block in virtualhost_blocks:
            # For each block, search for the ServerName directive
            match = re.search(r'ServerName\s+(\S+)', block)
            if match:
                server_names.add(match.group(1))
        return server_names
