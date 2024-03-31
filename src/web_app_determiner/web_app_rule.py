from typing import NamedTuple, Optional
import re


# class AuthMethod(NamedTuple):
#     type: str
#
# class UserAndPwdAuthMethod(AuthMethod):


class WebAppRule:
    def __init__(self, name: str, identifier: str, ver_url_path: Optional[str], ver_element: str):
        self.name = name
        self.identifier = identifier
        self.ver_element = ver_element
        self.ver_url_path = ver_url_path
        # auth_method: Optional[AuthMethod]

        # Compile the regular expression pattern for better performance
        self.id_pattern = WebAppRule._compile_regex_pattern(self.identifier)
        self.ver_pattern = WebAppRule._compile_regex_pattern(self.ver_element)

    @staticmethod
    def _compile_regex_pattern(pattern: str) -> re.Pattern[str]:
        try:
            return re.compile(pattern)
        except re.error:
            raise ValueError(f"Invalid regex pattern: '{pattern}'")

    def matches(self, html_content: str) -> bool:
        return bool(self.id_pattern.search(html_content))

    def find_version(self, html_content: str) -> Optional[str]:
        match = self.ver_pattern.search(html_content)
        if match:
            return match.group(1)
        else:
            return None
