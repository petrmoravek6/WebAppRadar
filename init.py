from typing import Optional
from src.exceptions import FatalError
from src.latest_version.full_info_fetcher import FullInfoFetcher
from src.latest_version.release_fetcher.method.endoflife import EndOfLifeReleaseFetcherMethod
from src.latest_version.release_fetcher.method.github import GitHubReleaseFetcherMethod
from src.latest_version.release_fetcher.release_fetcher import ReleaseFetcher
from src.latest_version.semantic_version_comparator import SemanticVersionComparator
from src.open_port_scanner.nmap_open_port_scanner import NMapOpenPortScanner
from src.scan_repository.mongo_scan_repository import MongoScanRepository
from src.ssh_client.p_key_paramiko_ssh_client import PrivateKeyCipher
from src.ssh_client.p_key_paramiko_ssh_client import PrivateKeyParamikoSSHClient
from src.ssh_client.pwd_paramiko_ssh_client import PasswordParamikoSSHClient
from src.vhost_net_scanner.local_web_server_vhosts_net_scanner import LocalWebServerVhostNetScanner
from src.vhosts_commands.apache2_vhosts_cmds import Apache2VhostsCmds
from src.web_app_radar import WebAppRadar
from src.web_server_scanner.open_port_web_server_scanner import OpenPortWebServerScanner
from src.vhost_discoverer.ssh_agent_vhost_discoverer import SshAgentVhostDiscoverer
from src.vhosts_commands.nginx_vhosts_cmds import NginxVhostsCmds
from src.hostname_resolver.socket_hostaname_resolver import SocketHostnameResolver
from src.subnet_validator.hostname_subnet_validator import HostnameSubnetValidator
from src.subnet_validator.ip_subnet_validator import IPSubnetValidator
import logging
import os
from src.web_app_determiner.html_content_parsing_method import HTMLContentParsingFromFileMethod
from src.web_app_determiner.web_app_determiner import WebAppDeterminer
from src.client_side_renderer.selenium_chrome_renderer import SeleniumChromeRenderer
from src.web_app_determiner.web_app_rule.authentication.auth_executor import AuthExecutor
from src.web_app_determiner.web_app_rule.json_deserializer import JsonWebAppRulesDeserializer
from src.config_parser import ConfigParser

logger = logging.getLogger(__name__)


def init_web_app_radar() -> Optional[WebAppRadar]:
    try:
        config_parser = ConfigParser()

        ssh_config = config_parser.get_ssh_config()
        ssh_method = ssh_config.get('method')
        ssh_user = ssh_config.get('username')

        if ssh_method == 'private_key':
            path_to_private_key_file = ssh_config['path_to_private_key_file']
            cipher_type = PrivateKeyCipher[ssh_config['private_key_cipher']]
            ssh_client = PrivateKeyParamikoSSHClient(path_to_private_key_file, cipher_type)
        else:
            ssh_password = ssh_config.get('path_to_password_file')
            ssh_client = PasswordParamikoSSHClient(ssh_password)

        hostname_resolver = SocketHostnameResolver()
        ip_validator = IPSubnetValidator()
        hostname_validator = HostnameSubnetValidator(hostname_resolver, ip_validator)
        web_server_cmds = (NginxVhostsCmds(), Apache2VhostsCmds())

        vhosts_discoverer = SshAgentVhostDiscoverer(ssh_client, web_server_cmds, ssh_user)

        open_port_scanner = NMapOpenPortScanner()
        web_server_scanner = OpenPortWebServerScanner(open_port_scanner)

        scanner = LocalWebServerVhostNetScanner(web_server_scanner, vhosts_discoverer, hostname_validator)

        web_apps_json_path = os.path.join(os.path.dirname(__file__), 'web-apps.json')
        renderer = SeleniumChromeRenderer()
        det_methods = [HTMLContentParsingFromFileMethod(renderer,
                                                        AuthExecutor(renderer),
                                                        web_apps_json_path,
                                                        JsonWebAppRulesDeserializer())]
        web_app_determiner = WebAppDeterminer(det_methods)

        release_methods = {
            "Atlassian Jira": EndOfLifeReleaseFetcherMethod("jira-software"),
            "Atlassian Confluence": EndOfLifeReleaseFetcherMethod("confluence"),
            "JFrog Artifactory Pro": EndOfLifeReleaseFetcherMethod("artifactory"),
            "Prometheus": EndOfLifeReleaseFetcherMethod("prometheus"),
            "Grafana": EndOfLifeReleaseFetcherMethod("grafana"),
            "GitLab": EndOfLifeReleaseFetcherMethod("gitlab"),
            "Zabbix": EndOfLifeReleaseFetcherMethod("zabbix"),
            "Graylog": EndOfLifeReleaseFetcherMethod("graylog"),
            "Keycloak": EndOfLifeReleaseFetcherMethod("keycloak"),
            "Bareos": GitHubReleaseFetcherMethod('bareos', 'bareos', "name",
                                                 r'\S*\s*(\d+\.\d+.\d+)'),
            "Snipe-IT": GitHubReleaseFetcherMethod('snipe', 'snipe-it', "name",
                                                   r'v(\d+\.\d+.\d+)')
        }

        release_fetcher = ReleaseFetcher(release_methods)
        full_info_fetcher = FullInfoFetcher(release_fetcher, dict(), SemanticVersionComparator())

        mongo_connection_str = os.getenv('MONGO_URI')
        if not mongo_connection_str:
            raise Exception("MONGO_URI env (connection string for MongoDB) not defined")
        mongo_scan_repository = MongoScanRepository(mongo_connection_str)

        return WebAppRadar(scanner, web_app_determiner, full_info_fetcher, mongo_scan_repository)
    except FatalError as fe:
        logger.error(f"Fatal error: {str(fe)}")
        logger.debug(f"Fatal error details: {fe.debug_msg}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
