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
from .settings import Settings
from .subscriptions import Subscriptions
from .links import Links
from .custom_geo import CustomGeo
from .xray import Xray
from .hosts import Hosts

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
        self.settings = Settings(self)
        self.subscriptions = Subscriptions(self)
        self.links = Links(self)
        self.custom_geo = CustomGeo(self)
        self.xray = Xray(self)
        self.hosts = Hosts(self)

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = kwargs.pop("headers", {})

        if self._csrf and method.upper() != "GET":
            headers["X-CSRF-Token"] = self._csrf

        try:
            resp = self.session.request(method, url, headers=headers, timeout=30, **kwargs)
        except requests.RequestException as e:
            raise ThreeXuiError(f"Ошибка сети: {e}")

        if resp.status_code == 401:
            raise AuthError("Не авторизован. Выполните login() или укажите token.")

        try:
            data = resp.json()
        except ValueError:
            raise ThreeXuiError(f"Панель вернула не JSON: {resp.status_code} {resp.text[:200]}")

        if not data.get("success", False):
            msg = data.get("msg", "Неизвестная ошибка панели")
            raise APIError(msg, data)

        return data.get("obj", data)

    def login(self, username: Optional[str] = None, password: Optional[str] = None,
              two_factor_code: Optional[str] = None):
        """авторизация по логину/паролю. Получает CSRF и cookie"""
        self._username = username or self._username
        self._password = password or self._password
        if not self._username or not self._password:
            raise AuthError("Нужны username и password для login()")

        data = self._request("GET", "login")
        self._csrf = data.get("csrfToken") or data.get("obj", {}).get("csrfToken")
        if not self._csrf:
            raise AuthError("Не удалось получить CSRF-токен")

        payload = {"username": self._username, "password": self._password}
        if two_factor_code:
            payload["twoFactorCode"] = two_factor_code

        self._request("POST", "login", data=payload)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.session.close()
