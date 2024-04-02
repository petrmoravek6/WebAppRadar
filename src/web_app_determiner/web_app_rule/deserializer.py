from abc import ABC, abstractmethod
from typing import Collection
from src.web_app_determiner.web_app_rule.web_app_rule import WebAppRule


class IWebAppRuleDeserializer(ABC):
    @abstractmethod
    def deserialize(self, data: str) -> Collection[WebAppRule]:
        pass
