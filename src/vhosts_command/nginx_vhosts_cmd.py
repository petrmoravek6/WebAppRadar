from vhosts_cmd import VhostsCmd


class NginxVhostsCmd(VhostsCmd):
    def get_all_vhosts(self) -> str:
        return 'cat /etc/nginx/sites-enabled/* | sed -r -e 's/[ \t]*$//' -e 's/^[ \t]*//' -e 's/^#.*$//' -e 's/[ \t]*#.*$//' -e '/^$/d' | sed -e ':a;N;$!ba;s/\([^;\{\}]\)\n/\1 /g' | grep -P 'server_name[ \t]' | grep -v '\$' | grep '\.' | sed -r -e 's/(\S)[ \t]+(\S)/\1\n\2/g' -e 's/[\t ]//g' -e 's/;//' -e 's/server_name//' | sort | uniq | xargs -L1'