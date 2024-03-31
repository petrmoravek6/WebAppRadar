from abc import ABC, abstractmethod


class IClientSideRenderer(ABC):
    @abstractmethod
    def get_page_content(self, host: str) -> str:
        pass
