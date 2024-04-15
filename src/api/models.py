from flask_restx import fields


def subnet_model(api):
    return api.model('SubnetInput', {
        'subnets': fields.String(required=True,
                                 description='Comma-separated subnets or IP addreses (or combination of both) to be scanned',
                                 example='192.168.0.0/24,192.168.68.68')
    })


def result_model(api):
    return api.model('ScanResult', {
        'id': fields.String(description='Result ID', example='471edecd-6f4a-4bf1-bc50-7aeb1a6af79a'),
        'completed_at': fields.DateTime(description='Timestamp when the scan was completed',
                                        example='2024-04-13T19:40:36.323496'),
        'status': fields.String(description='Flag indicating whether the scan was successful or failed',
                                example='success')
    })


def hostname_info_model(api):
    return api.model('HostnameInfo', {
        'hostname': fields.String(required=True, description='Hostname of the scanned device',
                                  example='www.example.com'),
        'name': fields.String(required=False, description='Name of the web application', example='GitLab'),
        'version': fields.String(required=False, description='Current version of the web application', example='5.1.0'),
        'latest_version': fields.String(required=False, description='Latest available version of the web application',
                                        example='6.2.3'),
        'latest_cycle_version': fields.String(required=False,
                                              description='Latest version of the web application regarding the current cycle version (MAJOR.MINOR)',
                                              example='5.1.8'),
        'eol': fields.Boolean(required=False,
                              description='Flag indicating whether the current version reached EOL support',
                              example=True),
        'eol_date': fields.String(required=False, description='End of Life date of the current version',
                                  example='2019-04-13')
    })


def result_detail_model(api, hostname_info_model):
    return api.model('ResultDetail', {
        'id': fields.String(attribute='_id', description='Scan ID', example='471edecd-6f4a-4bf1-bc50-7aeb1a6af79a'),
        'completed_at': fields.String(description='Timestamp when the scan was completed',
                                      example='2024-04-13T19:40:36.323496'),
        'status': fields.String(description='Flag indicating whether the scan was successful or failed',
                                example='success'),
        'subnets': fields.String(description='Subnets scanned', example='192.168.68.68/24'),
        'web_apps': fields.List(fields.Nested(hostname_info_model),
                                description='List of web applications discovered and their information')
    })
