from src.open_port_scanner.nmap_open_port_scanner import NMapOpenPortScanner
from src.ssh_client.p_key_paramiko_ssh_client import PrivateKeyCipher
from src.ssh_client.p_key_paramiko_ssh_client import PrivateKeyParamikoSSHClient
from src.vhost_net_scanner.local_web_server_vhosts_net_scanner import LocalVhostsNetScanner
from src.web_server_scanner.open_port_web_server_scanner import OpenPortWebServerScanner
from src.vhost_discoverer.ssh_agent_vhost_discoverer import SshAgentVhostDiscoverer
from src.vhosts_commands.nginx_vhosts_cmds import NginxVhostsCmds
from src.hostname_resolver.socket_hostaname_resolver import SocketHostnameResolver
from src.subnet_validator.pyt_hostname_subnet_validator import PytHostnameSubnetValidator
from src.subnet_validator.pyt_ip_subnet_validator import PytIPSubnetValidator
import logging
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import os
from src.web_app_determiner.html_content_parsing_method import HTMLContentParsingFromFileMethod
from src.web_app_determiner.web_app_determiner import WebAppDeterminer
from src.client_side_renderer.selenium_chrome_renderer import SeleniumChromeRenderer
from src.web_app_determiner.web_app_rule.authentication.auth_executor import AuthExecutor
from src.web_app_determiner.web_app_rule.json_deserializer import JsonWebAppRulesDeserializer

logging.basicConfig(level=logging.DEBUG,
                    filename='app.log',  # Output file
                    filemode='a',  # Append mode
                    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')

app = Flask(__name__)
api = Api(app, version='1.0', title='WebAppRadar API',
          description='System for detection and monitoring of versions of web applications in internal network '
                      'environments',
          )

ns = api.namespace('scan', description='Scan operations')

scan_model = api.model('ScanModel', {
    'string_to_scan': fields.String(required=True, description='The string to scan', example="example string"),
})


@ns.route('/')
class Scan(Resource):
    @ns.doc('scan_string',
            description='Scan a provided string. Submit a string to scan, and the API will return the scanned string.',
            responses={
                200: 'Success',
                400: 'Validation Error'
            },
            body=scan_model  # Indicates the body should follow the scan_model structure
            )
    @ns.expect(scan_model)
    def post(self):
        '''Scan a provided string'''
        if 'string_to_scan' in request.json and request.json['string_to_scan'].strip():
            return {'message': 'Scanned string', 'data': request.json['string_to_scan']}
        else:
            api.abort(400, "string_to_scan is required and cannot be empty.")


if __name__ == '__main__':
    app.run(debug=True)





# exit(0)
# web_apps_json_path = os.path.join(os.path.dirname(__file__), 'web-apps.json')
# renderer = SeleniumChromeRenderer()
# det_methods = [HTMLContentParsingFromFileMethod(renderer,
#                                                 AuthExecutor(renderer),
#                                                 web_apps_json_path,
#                                                 JsonWebAppRulesDeserializer())]
# resolver = WebAppDeterminer(det_methods)
# res4 = resolver.detect_web_app_info("graylog.quanti.cz/")
# print(res4.name, "  ", res4.version)
#
# from src.latest_version.release_fetcher.method.github import GitHubReleaseFetcherMethod
#
# gh = GitHubReleaseFetcherMethod()
# res = gh.fetch_cycle_info('bareos', 'bareos', "name", r'\S*\s*(\d+\.\d+.\d+)')
#
# nm = NMapOpenPortScanner()
# ws_sc = OpenPortWebServerScanner(nm)
#
# sc = PrivateKeyParamikoSSHClient('XXX', PrivateKeyCipher.RSA)
# nginx_cmd = NginxVhostsCmds()
# vhosts_dis = SshAgentVhostDiscoverer(sc, (nginx_cmd,), 'XXXX')
#
# hnr = SocketHostnameResolver()
# x = hnr.get_ip('192.168.68.119')
# ip_subnet_validator = PytIPSubnetValidator()
# hostname_subnet_validator = PytHostnameSubnetValidator(hnr, ip_subnet_validator)
#
# f1 = LocalWebServerVhostsNetScanner(ws_sc, vhosts_dis, hostname_subnet_validator)
# res = f1.get_all_vhosts(('192.168.68.140', '192.168.68.119'))
# print(res)
