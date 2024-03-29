from src.vhosts_commands.vhosts_cmds import IVhostsCmds
import re


class NginxVhostsCmds(IVhostsCmds):
    def is_web_server_running(self) -> str:
        return ("systemctl -q is-active nginx || (service nginx status > /dev/null 2>&1 && service nginx status | grep "
                "-q 'active (running)')")

    def get_content_from_server(self) -> str:
        return "cat /etc/nginx/sites-enabled/*"

    def get_all_vhosts_from_content(self, content: str) -> set[str]:
        # Step 1: Process each line (trim, remove comments)
        lines = content.splitlines()
        processed_lines = []
        for line in lines:
            clean_line = line.strip()
            # Remove comments, skip empty lines
            if clean_line and not clean_line.startswith('#'):
                processed_lines.append(re.sub(r'\s*#.*$', '', clean_line))  # Inline comment removal

        # Step 2: Concatenate lines properly
        concatenated = ' '.join(processed_lines)

        # Step 3: Extract server names
        server_names_raw = re.findall(r'server_name\s+([^;$]+)', concatenated)

        # Step 4: Clean up and extract unique server names
        server_names = set()
        for name in server_names_raw:
            try:
                for part in re.split(r'\s+', name.strip()):
                    clean_part = part.replace(';', '').strip()
                    # Ensure it looks like a domain and doesn't have variables
                    if '.' in clean_part and not '$' in clean_part:
                        server_names.add(clean_part)
            # unexpected error
            except Exception:
                continue

        return server_names
