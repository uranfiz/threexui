import requests
from typing import Optional, Dict, Any, List
from .exceptions import AuthError, APIError, ThreeXuiError
from .models import Client, Inbound
from .clients import Clients
from .inbounds import Inbounds
from .groups import Groups
from .nodes import Nodes
from .server import Server
from .generators import Generators

class Panel:
    """
    Клиент для панели 3x-ui

    Пример:
        panel = Panel("https://example.com:2053", token="YOUR_TOKEN")
        panel.clients.add("user1", inbound_ids=[1], total_gb=100)
        print(panel.clients.links("user1"))
    """

    def __init__(self, base_url: str, token: Optional[str] = None,
                 username: Optional[str] = None, password: Optional[str] = None,
                 verify_ssl: bool = True):
        self.base_url = base_url.rstrip("/")
        if self.base_url.endswith("/panel"):
            self.base_url = self.base_url[:-6]

        self.session = requests.Session()
        self.session.verify = verify_ssl
        self._token = token
        self._username = username
        self._password = password
        self._csrf = None

        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

        self.clients = Clients(self)
        self.inbounds = Inbounds(self)
        self.groups = Groups(self)
        self.nodes = Nodes(self)
        self.server = Server(self)
        self.generators = Generators(self)

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:.
        pass

    def login(self, username=None, password=None, two_factor_code=None):
        pass
