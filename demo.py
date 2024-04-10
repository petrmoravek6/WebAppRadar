import os

from src.client_side_renderer.selenium_chrome_renderer import SeleniumChromeRenderer
from src.hostname_resolver.socket_hostaname_resolver import SocketHostnameResolver
from src.latest_version.full_info_fetcher import FullInfoFetcher
from src.latest_version.release_fetcher.release_fetcher import ReleaseFetcher
from src.latest_version.semantic_version_comparator import SemanticVersionComparator
from src.open_port_scanner.nmap_open_port_scanner import NMapOpenPortScanner
from src.ssh_client.pwd_paramiko_ssh_client import PasswordParamikoSSHClient
from src.subnet_validator.pyt_hostname_subnet_validator import PytHostnameSubnetValidator
from src.subnet_validator.pyt_ip_subnet_validator import PytIPSubnetValidator
from src.vhost_discoverer.ssh_agent_vhost_discoverer import SshAgentVhostDiscoverer
from src.vhost_net_scanner.local_web_server_vhosts_net_scanner import LocalVhostsNetScanner
from src.vhosts_commands.apache2_vhosts_cmds import Apache2VhostsCmds
from src.vhosts_commands.nginx_vhosts_cmds import NginxVhostsCmds
from src.web_app_determiner.html_content_parsing_method import HTMLContentParsingFromFileMethod
from src.web_app_determiner.web_app_determiner import WebAppDeterminer
from src.web_app_determiner.web_app_rule.authentication.auth_executor import AuthExecutor
from src.web_app_determiner.web_app_rule.json_deserializer import JsonWebAppRulesDeserializer
from src.web_server_scanner.open_port_web_server_scanner import OpenPortWebServerScanner
from src.web_app_radar import WebAppRadar

ssh_pwd = 'test'
ssh_user = 'test'
web_apps_json_path = os.path.join(os.path.dirname(__file__), 'web-apps.json')
subnet_to_scan = '192.168.0.24/29'

# =======================================================================================

hostname_resolver = SocketHostnameResolver()
ip_validator = PytIPSubnetValidator()
hostname_validator = PytHostnameSubnetValidator(hostname_resolver, ip_validator)

web_server_cmds = (NginxVhostsCmds(), Apache2VhostsCmds())
ssh_client = PasswordParamikoSSHClient(ssh_pwd)
vhosts_discoverer = SshAgentVhostDiscoverer(ssh_client, web_server_cmds, ssh_user)

open_port_scanner = NMapOpenPortScanner()
web_server_scanner = OpenPortWebServerScanner(open_port_scanner)

renderer = SeleniumChromeRenderer()
det_methods = [HTMLContentParsingFromFileMethod(renderer,
                                                AuthExecutor(renderer),
                                                web_apps_json_path,
                                                JsonWebAppRulesDeserializer())]
web_app_determiner = WebAppDeterminer(det_methods)
scanner = LocalVhostsNetScanner(web_server_scanner, vhosts_discoverer, hostname_validator)
release_fetcher = ReleaseFetcher()
full_info_fetcher = FullInfoFetcher(release_fetcher, dict(), SemanticVersionComparator())

# =======================================================================================

web_app_radar = WebAppRadar(scanner, web_app_determiner, full_info_fetcher)
print("STARTING TO SCAN...")
scan_result = web_app_radar.run((subnet_to_scan,))
if scan_result and len(scan_result) != 0:
    print("SCAN RESULT:\n")
else:
    print("Unexpected error: DEMO scan didn't find any valuable information")
for res in scan_result:
    print(f'- HOSTNAME: {res.hostname}')
    if res.full_web_app_info:
        print(f'   INFO: {str(res.full_web_app_info)}')
    else:
        print("   INFO: UNKNOWN")
    print('\n', end='')
