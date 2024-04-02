from abc import abstractmethod, ABC
from typing import Optional


class IAuthVisitor(ABC):
    @abstractmethod
    def visit_user_and_pwd_auth(self, auth):
        pass


class Auth(ABC):
    def __init__(self, method: str, auth_path: Optional[str] = None):
        self.method = method
        self.auth_path = auth_path

    @abstractmethod
    def accept(self, visitor: IAuthVisitor):
        pass
