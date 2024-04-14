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

SCAN_LOCK = Lock()

logging.basicConfig(level=logging.DEBUG,
                    filename='app.log',  # Output file
                    filemode='a',  # Append mode
                    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

from flask import Flask, request
from flask_restx import Api, Resource, fields
from pymongo import MongoClient
import uuid
import datetime
import threading
import ipaddress

app = Flask(__name__)
api = Api(app, version='1.0', title='WebApp Radar API',
          description='API for scanning web applications in given subnets')
app.config['RESTX_MASK_SWAGGER'] = False

# MongoDB client setup
mongo_connection_str = os.getenv('MONGO_URI')
if not mongo_connection_str:
    raise Exception("MONGO_URI env (connection string for MongoDB) not defined")
client = MongoClient(mongo_connection_str)
db = client.webapp_radar

# Input and output models
subnet_model = api.model('SubnetInput', {
    'subnets': fields.String(required=True, description='Comma-separated subnets or IP addreses (or combination of both) to be scanned', example='192.168.0.0/24,192.168.68.68')
})

result_model = api.model('ScanResult', {
    'id': fields.String(description='Result ID'),
    'completed_at': fields.DateTime(description='Timestamp when the scan was completed', example='2024-04-13T19:40:36.323496'),
    'status': fields.String(description='Flag indicating whether the scan was successful or failed', example='success')
})

hostname_info_model = api.model('HostnameInfo', {
    'hostname': fields.String(required=True, description='Hostname of the scanned device'),
    'name': fields.String(required=False, description='Name of the web application'),
    'version': fields.String(required=False, description='Current version of the web application', example='5'),
    'latest_version': fields.String(required=False, description='Latest available version of the web application', example='7'),
    'latest_cycle_version': fields.String(required=False, description='Latest release cycle version of the web application', example='6'),
    'eol': fields.Boolean(required=False, description='End of Life status of the web application'),
    'eol_date': fields.String(required=False, description='End of Life date of the web application')
})

result_detail_model = api.model('ResultDetail', {
    'id': fields.String(attribute='_id', description='Scan ID'),
    'completed_at': fields.String(description='Timestamp when the scan was completed', example='2024-04-13T19:40:36.323496'),
    'status': fields.String(description='Flag indicating whether the scan was successful or failed', example='success'),
    'subnets': fields.String(description='Subnets scanned'),
    'web_apps': fields.List(fields.Nested(hostname_info_model), description='List of web applications discovered and their information')
})


def validate_subnets(subnets):
    subnet_list = subnets.split(',')
    try:
        for subnet in subnet_list:
            ipaddress.ip_network(subnet, strict=False)
        return True
    except ValueError:
        return False


def run_scan(subnets: str, scan_id: str, web_app_radar: WebAppRadar = None):
    SCAN_LOCK.acquire()

    status = 'success'
    scan_results = tuple()
    try:
        # scan_results = web_app_radar.run(subnets.split(','))
        scan_results = [
            HostnameInfo('192.168.120.100', FullWebAppInfo('Jira', '5', '7', '6', eol=False, eol_date=datetime.date.today())),
            HostnameInfo('192.168.120.101', FullWebAppInfo('Confluence', '8', '9', '8.2')),
            HostnameInfo('192.168.120.102', FullWebAppInfo('Bareos', '6', '7')),
            HostnameInfo('192.168.120.103', FullWebAppInfo('Git', '6')),
            HostnameInfo('192.168.120.104', FullWebAppInfo('Test')),
            HostnameInfo('192.168.120.105', None),
        ]
        time.sleep(20)
    except FatalError as fe:
        logger.error(f"Fatal error: {str(fe)}")
        logger.debug(f"Fatal error details: {fe.debug_msg}")
        status = 'fail'
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        status = 'fail'
    finally:
        document = {
            '_id': scan_id,
            'completed_at': datetime.datetime.now().isoformat(),
            'status': status,
            'subnets': subnets,
            'web_apps': [info.to_dict() for info in scan_results]
        }

        # Insert the document into MongoDB
        db.results.insert_one(document)
        SCAN_LOCK.release()


@api.route('/scan')
class Scan(Resource):
    @api.doc('start_scan', description="asdasasd")
    @api.expect(subnet_model)
    @api.response(400, 'Invalid input')
    @api.response(405, 'Scan already in progress')
    @api.response(202, 'Scan started')
    def post(self):
        data = request.json
        subnets = data.get('subnets', '')
        if not subnets or not validate_subnets(subnets):
            api.abort(400, 'Invalid or empty subnet input')
        scan_id = str(uuid.uuid4())
        if SCAN_LOCK.locked():
            api.abort(405, 'Scan already in progress')
        thread = threading.Thread(target=run_scan, args=(subnets, scan_id))
        thread.start()
        return {'message': 'Scan started', 'scan_id': scan_id}, 202


@api.route('/result')
class ResultList(Resource):
    @api.doc('list_results', description="asdasasd")
    @api.marshal_list_with(result_model)
    def get(self):
        results = list(db.results.find({}, {'_id': 1, 'completed_at': 1, 'status': 1}))
        # Sort the results by 'completed_at' field in ascending order
        results.sort(key=lambda r: r['completed_at'], reverse=True)
        return [{'id': str(result['_id']), 'completed_at': result['completed_at'], 'status': result['status']} for result in results]


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
