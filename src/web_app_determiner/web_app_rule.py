import json
from abc import abstractmethod, ABC
from typing import NamedTuple, Optional, Collection
import re


# class AuthMethod(NamedTuple):
#     type: str
#
# class UserAndPwdAuthMethod(AuthMethod):


class WebAppRule:
    def __init__(self, name: str,
                 identifier: str,
                 version_path: Optional[str],
                 version: str,
                 auth_method: Optional[bool] = None):
        self.name = name
        self.identifier = identifier
        self.version = version
        self.version_path = version_path
        self.auth_method = auth_method
        # auth_method: Optional[AuthMethod]

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
            rule = WebAppRule(
                name=item.get('name'),
                identifier=item.get('identifier'),
                version_path=item.get('version_path', None),
                version=item.get('version'),
                auth_method=item.get('auth_method', None)
            )
            rules.append(rule)
        return rules
