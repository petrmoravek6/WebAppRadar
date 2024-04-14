import time
from src.exceptions import FatalError
from src.latest_version.full_web_app_info import FullWebAppInfo
from src.open_port_scanner.nmap_open_port_scanner import NMapOpenPortScanner
from src.ssh_client.p_key_paramiko_ssh_client import PrivateKeyCipher
from src.ssh_client.p_key_paramiko_ssh_client import PrivateKeyParamikoSSHClient
from src.vhost_net_scanner.local_web_server_vhosts_net_scanner import LocalVhostsNetScanner
from src.web_app_radar import WebAppRadar, HostnameInfo
from src.web_server_scanner.open_port_web_server_scanner import OpenPortWebServerScanner
from src.vhost_discoverer.ssh_agent_vhost_discoverer import SshAgentVhostDiscoverer
from src.vhosts_commands.nginx_vhosts_cmds import NginxVhostsCmds
from src.hostname_resolver.socket_hostaname_resolver import SocketHostnameResolver
from src.subnet_validator.pyt_hostname_subnet_validator import PytHostnameSubnetValidator
from src.subnet_validator.pyt_ip_subnet_validator import PytIPSubnetValidator
import logging
import os
from src.web_app_determiner.html_content_parsing_method import HTMLContentParsingFromFileMethod
from src.web_app_determiner.web_app_determiner import WebAppDeterminer
from src.client_side_renderer.selenium_chrome_renderer import SeleniumChromeRenderer
from src.web_app_determiner.web_app_rule.authentication.auth_executor import AuthExecutor
from src.web_app_determiner.web_app_rule.json_deserializer import JsonWebAppRulesDeserializer
from threading import Lock
from flask import Flask, request
from flask_restx import Api, Resource
import uuid
from src.api.functions import init_db_connection, run_scan, validate_subnets
import threading
from src.api import models

logging.basicConfig(level=logging.DEBUG,
                    filename='app.log',  # Output file
                    filemode='a',  # Append mode
                    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')

SCAN_LOCK = Lock()
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app, version='1.0', title='WebApp Radar API',
          description='API for scanning web applications in given subnets')
app.config['RESTX_MASK_SWAGGER'] = False
db = init_db_connection()
subnet_model = models.subnet_model(api)
result_model = models.result_model(api)
hostname_info_model = models.hostname_info_model(api)
result_detail_model = models.result_detail_model(api, hostname_info_model)


@api.route('/scan')
class Scan(Resource):
    @api.doc('start_scan', description="Initializes new scan of given subnets/IPs. "
                                       "Immediately returns the scan ID while the scan is running in background. "
                                       "Only one scan can run at a time.")
    @api.expect(subnet_model)
    @api.response(400, 'Invalid input. Correct format: IPs or subnets separated by a comma')
    @api.response(405, 'Another scan already in progress')
    @api.response(202, 'Scan started')
    def post(self):
        data = request.json
        subnets = data.get('subnets', '')
        if not subnets or not validate_subnets(subnets):
            api.abort(400, 'Invalid or empty subnet input')
        scan_id = str(uuid.uuid4())
        if SCAN_LOCK.locked():
            api.abort(405, 'Scan already in progress')
        thread = threading.Thread(target=run_scan, args=(subnets, SCAN_LOCK, scan_id))
        thread.start()
        return {'message': 'Scan started', 'scan_id': scan_id}, 202


@api.route('/result')
class ResultList(Resource):
    @api.doc('list_results', description="Return IDs, timestamp completitions and statues of all historical results")
    @api.marshal_list_with(result_model)
    def get(self):
        results = list(db.results.find({}, {'_id': 1, 'completed_at': 1, 'status': 1}))
        # Sort the results by 'completed_at' field in ascending order
        results.sort(key=lambda r: r['completed_at'], reverse=True)
        return [{'id': str(result['_id']), 'completed_at': result['completed_at'], 'status': result['status']} for
                result in results]


@api.route('/result/<id>')
@api.param('id', 'The result identifier')
class Result(Resource):
    @api.doc('get_result', description="Retrieves detailed information about a specific scan.")
    @api.response(404, 'Result not found')
    @api.marshal_with(result_detail_model)
    def get(self, id):
        result = db.results.find_one({'_id': id})
        if result:
            return result
        else:
            api.abort(404, 'Result with provided ID not found')
