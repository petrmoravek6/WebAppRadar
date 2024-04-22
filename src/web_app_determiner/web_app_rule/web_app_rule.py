from typing import Optional
import re
from src.web_app_determiner.web_app_rule.authentication.auth import Auth


class WebAppRule:
    def __init__(self, web_app_name: str,
                 identifier: str,
                 version_string: Optional[str],
                 version_path: Optional[str] = None,
                 auth: Optional[Auth] = None):
        self.web_app_name = web_app_name
        self.identifier = identifier
        self.version_string = version_string
        self.version_path = version_path
        self.auth = auth

        # Compile the regular expression pattern for better performance
        self.id_pattern = WebAppRule._compile_regex_pattern(self.identifier)
        if self.version_string is not None:
            self.ver_pattern = WebAppRule._compile_regex_pattern(self.version_string)

    @staticmethod
    def _compile_regex_pattern(pattern: str) -> re.Pattern[str]:
        try:
            return re.compile(pattern)
        except re.error:
            raise ValueError(f"Invalid regex pattern: {pattern}")

    def matches(self, html_content: str) -> bool:
        return bool(self.id_pattern.search(html_content))

    def find_version(self, html_content: str) -> Optional[str]:
        if self.version_string is None:
            return None
        match = self.ver_pattern.search(html_content)
        if match:
            return match.group(1)
        else:
            return None
