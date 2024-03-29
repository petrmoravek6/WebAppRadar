from src.vhosts_commands.vhosts_cmds import IVhostsCmds
import re


class Apache2VhostsCmds(IVhostsCmds):
    def is_web_server_running(self) -> str:
        return ("systemctl -q is-active apache2 || (service apache2 status > /dev/null 2>&1 && service apache2 status "
                "| grep -q 'active (running)')")

    def get_content_from_server(self) -> str:
        return "cat /etc/apache2/sites-enabled/*"

    def get_all_vhosts_from_content(self, content: str) -> set[str]:
        lines = content.splitlines()
        lines_without_comments = []
        for line in lines:
            clean_line = line.strip()
            # Remove comments, skip empty lines
            if clean_line and not clean_line.startswith('#'):
                lines_without_comments.append(re.sub(r'\s*#.*$', '', clean_line))

        # Using a set to store server names to ensure uniqueness
        server_names = set()
        for line in lines_without_comments:
            # For each line, search for the ServerName directive
            match = re.search(r'ServerName\s+(\S+)', line)
            if match:
                server_names.add(match.group(1))
        return server_names
