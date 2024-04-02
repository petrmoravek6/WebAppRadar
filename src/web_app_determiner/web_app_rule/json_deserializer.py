import json
from typing import Collection
from src.web_app_determiner.web_app_rule.authentication.html_elem_param import HTMLElementParam
from src.web_app_determiner.web_app_rule.authentication.user_and_pwd_auth import UserAndPwdAuth
from src.web_app_determiner.web_app_rule.deserializer import IWebAppRuleDeserializer
from src.web_app_determiner.web_app_rule.web_app_rule import WebAppRule


class JsonWebAppRuleDeserializer(IWebAppRuleDeserializer):
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
                    user_box_params = [HTMLElementParam(k, v) for k, v in auth_data.get('user_box_params', [])]
                    pwd_box_params = [HTMLElementParam(k, v) for k, v in auth_data.get('pwd_box_params', [])]
                    auth_instance = UserAndPwdAuth(method, auth_path, user_box_params, pwd_box_params)

            rule = WebAppRule(
                name=item.get('name'),
                identifier=item.get('identifier'),
                version=item.get('version'),
                version_path=item.get('version_path', None),
                auth=auth_instance
            )
            rules.append(rule)
        return rules
