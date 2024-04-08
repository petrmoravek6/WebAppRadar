import time
from typing import Iterable, Optional
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from src.client_side_renderer.selenium_renderer import SeleniumRenderer
from src.web_app_determiner.web_app_rule.authentication.html_elem_param import HTMLElementParam
from src.web_app_determiner.web_app_rule.authentication.user_and_pwd_auth import UserAndPwdAuth
from src.web_app_determiner.web_app_rule.authentication.auth import IAuthVisitor
import logging

logger = logging.getLogger(__name__)


class AuthExecutor(IAuthVisitor):
    def __init__(self, renderer: SeleniumRenderer):
        self.renderer = renderer

    @staticmethod
    def get_xpath_params(params: Iterable[HTMLElementParam]) -> str:
        return ''.join(f"[@{param.key}='{param.value}']" for param in params)

    def _create_absolute_auth_path(self, relative_auth_path: str):
        # both current URL of the driver and relative path might contain '/' -> remove one
        if self.renderer.driver.current_url.endswith('/') and relative_auth_path.startswith('/'):
            return self.renderer.driver.current_url[:-1] + relative_auth_path
        return self.renderer.driver.current_url + relative_auth_path

    def visit_user_and_pwd_auth(self, auth: UserAndPwdAuth) -> Optional[str]:
        try:
            if auth.auth_path:
                abs_auth_path = self._create_absolute_auth_path(auth.auth_path)
                self.renderer.get_page_content(abs_auth_path)
            username_input_xpath = f"//input{AuthExecutor.get_xpath_params(auth.user_box_params)}"
            username_input = self.renderer.driver.find_element(By.XPATH, username_input_xpath)
            if not username_input:
                return None
            username_input.clear()
            username_input.send_keys(auth.username)

            password_input_xpath = f"//input{AuthExecutor.get_xpath_params(auth.pwd_box_params)}"
            password_input = self.renderer.driver.find_element(By.XPATH, password_input_xpath)
            if not password_input:
                return None
            password_input.clear()
            password_input.send_keys(auth.password)

            password_input.send_keys(Keys.ENTER)
            time.sleep(self.renderer.explicit_waiting)
            res = self.renderer.driver.page_source
            return res
        except Exception as e:
            logger.info(f"Exception during authentication: {e}")
            return None
