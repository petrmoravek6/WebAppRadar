import json
from typing import Collection
from src.web_app_determiner.web_app_rule.authentication.html_elem_param import HTMLElementParam
from src.web_app_determiner.web_app_rule.authentication.user_and_pwd_auth import UserAndPwdAuth
from src.web_app_determiner.web_app_rule.deserializer import IWebAppRulesDeserializer
from src.web_app_determiner.web_app_rule.web_app_rule import WebAppRule


class JsonWebAppRulesDeserializer(IWebAppRulesDeserializer):
    def deserialize(self, data: str) -> Collection[WebAppRule]:
        parsed_data = json.loads(data)
        rules = []
        for item in parsed_data:
            # Check if auth data is provided and not null
            auth_data = item.get('auth')
            auth_instance = None
            if auth_data:
                auth_path = auth_data.get('auth_path')
                # Determine the type of auth and create the appropriate instance
                method = auth_data.get('method')
                if method == 'username_and_password':
                    user_box_params = [HTMLElementParam(key=d['key'], value=d['value']) for d in
                                       auth_data.get('user_box_params', [])]
                    pwd_box_params = [HTMLElementParam(key=d['key'], value=d['value']) for d in
                                      auth_data.get('pwd_box_params', [])]
                    username = auth_data.get('username')
                    pwd = auth_data.get('password')
                    auth_instance = UserAndPwdAuth(method, user_box_params, pwd_box_params, username, pwd, auth_path)

            rule = WebAppRule(
                name=item.get('name'),
                identifier=item.get('identifier'),
                version=item.get('version'),
                version_path=item.get('version_path', None),
                auth=auth_instance
            )
            rules.append(rule)
        return rules
