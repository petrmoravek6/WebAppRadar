from src.vhosts_command.vhosts_cmd import IVhostsCmd
import re


class NginxVhostsCmd(IVhostsCmd):
    def is_web_server_running(self) -> str:
        return ("systemctl -q is-active nginx || (service nginx status > /dev/null 2>&1 && service nginx status | grep "
                "-q 'active (running)')")

    def get_content_from_server(self) -> str:
        return "cat /etc/nginx/sites-enabled/*"

    # return r"""cat /etc/nginx/sites-enabled/* | sed -r -e 's/[ \t]*$//' -e 's/^[ \t]*//' -e 's/^#.*$//' -e 's/[
    #         \t]*#.*$//' -e '/^$/d' | sed -e ':a;N;$!ba;s/\([^;\{\}]\)\n/\1 /g' | grep -P 'server_name[ \t]' | grep -v
    #         '\$' | grep '\.' | sed -r -e 's/(\S)[ \t]+(\S)/\1\n\2/g' -e 's/[\t ]//g' -e 's/;//' -e 's/server_name//' |
    #         sort | uniq | xargs -L1"""

    def get_all_vhosts_from_content(self, content: str) -> set[str]:
        # Step 1: Process each line (trim, remove comments)
        lines = content.splitlines()
        processed_lines = []
        for line in lines:
            clean_line = line.strip()
            # Remove comments, skip empty lines
            if clean_line and not clean_line.startswith('#'):
                processed_lines.append(re.sub(r'\s*#.*$', '', clean_line))  # Inline comment removal

        # Step 2: Concatenate lines properly (not fully replicated due to complexity)
        concatenated = ' '.join(processed_lines)  # Simplified approach

        # Step 3: Extract server names
        server_names_raw = re.findall(r'server_name\s+([^;$]+)', concatenated)

        # Step 4: Clean up and extract unique server names
        server_names = set()
        for name in server_names_raw:
            for part in re.split(r'\s+', name.strip()):
                clean_part = part.replace(';', '').strip()
                if '.' in clean_part and not '$' in clean_part:  # Ensure it looks like a domain and doesn't have variables
                    server_names.add(clean_part)

        return server_names
