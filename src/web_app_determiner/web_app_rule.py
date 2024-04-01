import json
import time
from abc import abstractmethod, ABC
from typing import NamedTuple, Optional, Collection, Iterable
import re
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from src.client_side_renderer.selenium_renderer import SeleniumRenderer


class HTMLElementParam(NamedTuple):
    key: str
    value: str


class IAuthVisitor:
    @abstractmethod
    def visit_user_and_pwd_auth(self, auth: UserAndPwdAuth):
        pass


class AuthExecutor(IAuthVisitor):
    @staticmethod
    def get_xpath_params(params: Iterable[HTMLElementParam]) -> str:
        return ''.join(f"[@{param.key}='{param.value}']" for param in params)

    def visit_user_and_pwd_auth(self, auth: UserAndPwdAuth) -> Optional[str]:
        try:
            username_input_xpath = f"//input{AuthExecutor.get_xpath_params(auth.user_box_params)}"
            username_input = self.renderer.driver.find_element(By.XPATH, username_input_xpath)
            username_input.clear()
            username_input.send_keys('your_username')

            password_input_xpath = f"//input{AuthExecutor.get_xpath_params(auth.pwd_box_params)}"
            password_input = self.renderer.driver.find_element(By.XPATH, password_input_xpath)
            password_input.clear()
            password_input.send_keys('your_password')

            password_input.send_keys(Keys.ENTER)
            time.sleep(self.renderer.explicit_waiting)
            res = self.renderer.driver.page_source
            return res
        except Exception:
            return None

    def __init__(self, renderer: SeleniumRenderer):
        self.renderer = renderer


class Auth:
    def __init__(self, method: str):
        self.method = method

    @abstractmethod
    def accept(self, visitor: IAuthVisitor):
        pass


class UserAndPwdAuth(Auth):
    def __init__(self, method: str, user_box_params: list[HTMLElementParam], pwd_box_params: list[HTMLElementParam]):
        super().__init__(method)
        self.user_box_params = user_box_params
        self.pwd_box_params = pwd_box_params

    def accept(self, visitor: IAuthVisitor):
        visitor.visit_user_and_pwd_auth(self)


class WebAppRule:
    def __init__(self, name: str,
                 identifier: str,
                 version: str,
                 version_path: Optional[str] = None,
                 auth: Optional[Auth] = None):
        self.name = name
        self.identifier = identifier
        self.version = version
        self.version_path = version_path
        self.auth = auth

        # Compile the regular expression pattern for better performance
        self.id_pattern = WebAppRule._compile_regex_pattern(self.identifier)
        self.ver_pattern = WebAppRule._compile_regex_pattern(self.version)

    @staticmethod
    def _compile_regex_pattern(pattern: str) -> re.Pattern[str]:
        try:
            return re.compile(pattern)
        except re.error:
            raise ValueError(f"Invalid regex pattern: {pattern}")

    def matches(self, html_content: str) -> bool:
        return bool(self.id_pattern.search(html_content))

    def find_version(self, html_content: str) -> Optional[str]:
        match = self.ver_pattern.search(html_content)
        if match:
            return match.group(1)
        else:
            return None


class IWebAppRuleDeserializer(ABC):
    @abstractmethod
    def deserialize(self, data: str) -> Collection[WebAppRule]:
        pass


class JsonWebAppRuleDeserializer(IWebAppRuleDeserializer):
    def deserialize(self, data: str) -> Collection[WebAppRule]:
        parsed_data = json.loads(data)
        rules = []
        for item in parsed_data:
            # Check if auth data is provided and not null
            auth_data = item.get('auth')
            auth_instance = None
            if auth_data:
                # Determine the type of auth and create the appropriate instance
                method = auth_data.get('method')
                if method == 'username_and_password':
                    user_box_params = [HTMLElementParam(k, v) for k, v in auth_data.get('user_box_params', [])]
                    pwd_box_params = [HTMLElementParam(k, v) for k, v in auth_data.get('pwd_box_params', [])]
                    auth_instance = UserAndPwdAuth(method, user_box_params, pwd_box_params)

            rule = WebAppRule(
                name=item.get('name'),
                identifier=item.get('identifier'),
                version=item.get('version'),
                version_path=item.get('version_path', None),
                auth=auth_instance
            )
            rules.append(rule)
        return rules
