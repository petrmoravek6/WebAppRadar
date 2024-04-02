from typing import Optional
import re
from src.web_app_determiner.web_app_rule.authentication.auth import Auth


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
