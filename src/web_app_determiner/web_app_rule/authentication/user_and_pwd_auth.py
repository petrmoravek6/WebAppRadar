from typing import Optional

from src.web_app_determiner.web_app_rule.authentication.auth import Auth
from src.web_app_determiner.web_app_rule.authentication.html_elem_param import HTMLElementParam
from src.web_app_determiner.web_app_rule.authentication.auth import IAuthVisitor


class UserAndPwdAuth(Auth):
    def __init__(self, method: str, auth_path: Optional[str],
                 user_box_params: list[HTMLElementParam], pwd_box_params: list[HTMLElementParam]):
        super().__init__(method, auth_path)
        self.user_box_params = user_box_params
        self.pwd_box_params = pwd_box_params

    def accept(self, visitor: IAuthVisitor):
        return visitor.visit_user_and_pwd_auth(self)
