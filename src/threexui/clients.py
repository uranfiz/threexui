from typing import List, Optional, Union
from datetime import datetime, timedelta
from .models import Client, ClientTraffic
from .exceptions import APIError, ThreeXuiError

class Clients:
    """Управление клиентами"""
    
    def __init__(self, panel):
        self.panel = panel

    def _traffic_to_bytes(self, gb: Optional[int]) -> int:
        if gb is None:
            return 0
        return int(gb * 1024**3)

    def _expiry_to_ms(self, expires: Union[timedelta, datetime, None]) -> int:
        if expires is None:
            return 0
        if isinstance(expires, timedelta):
            dt = datetime.now() + expires
        else:
            dt = expires
        return int(dt.timestamp() * 1000)

    def add(self, email: str, inbound_ids: List[int], 
            total_gb: Optional[int] = None,
            expires: Union[timedelta, datetime, None] = None,
            limit_ip: int = 0,
            **kwargs) -> Client:
        """создать клиента и привязать к inbounds"""
        total_bytes = self._traffic_to_bytes(total_gb)
        expiry_ms = self._expiry_to_ms(expires)
        
        payload = {
            "email": email,
            "inboundIds": inbound_ids,
            "totalGB": total_bytes,
            "expiryTime": expiry_ms,
            "limitIp": limit_ip,
        }
        payload.update(kwargs)
        
        data = self.panel._request("POST", "panel/api/clients/add", json=payload)
        return Client.model_validate(data.get("client", data))

    def get(self, email: str) -> Optional[Client]:
        """получить клиента по email"""
        try:
            data = self.panel._request("GET", f"panel/api/clients/get/{email}")
            return Client.model_validate(data)
        except APIError:
            return None

    def links(self, email: str) -> List[str]:
        """получить все ссылки (vless://, trojan://...) для клиента"""
        data = self.panel._request("GET", f"panel/api/clients/links/{email}")
        if isinstance(data, list):
            return data
        return data.get("links", [])

    def sub_links(self, sub_id: str) -> str:
        """получить ссылку-подписку по subId"""
        data = self.panel._request("GET", f"panel/api/clients/subLinks/{sub_id}")
        if isinstance(data, str):
            return data
        return data.get("link", "")

    def traffic(self, email: str) -> ClientTraffic:
        """получить статистику трафика клиента"""
        data = self.panel._request("GET", f"panel/api/clients/traffic/{email}")
        return ClientTraffic.model_validate(data)

    def reset_traffic(self, email: str):
        """сбросить счётчик трафика"""
        return self.panel._request("POST", f"panel/api/clients/resetTraffic/{email}")

    def delete(self, email: str, keep_traffic: bool = False):
        """удалить клиента. keep_traffic=True оставит записи статистики"""
        params = {"keepTraffic": "true" if keep_traffic else "false"}
        return self.panel._request("DELETE", f"panel/api/clients/del/{email}", params=params)

    def update(self, email: str, **fields) -> Client:
        """обновить поля клиента"""
        if "total_gb" in fields:
            fields["totalGB"] = self._traffic_to_bytes(fields.pop("total_gb"))
        if "expires" in fields:
            fields["expiryTime"] = self._expiry_to_ms(fields.pop("expires"))
            
        data = self.panel._request("POST", f"panel/api/clients/update/{email}", json=fields)
        return Client.model_validate(data)

    def online(self) -> List[str]:
        """список email'ов, которые сейчас онлайн"""
        data = self.panel._request("GET", "panel/api/clients/onlines")
        return data if isinstance(data, list) else data.get("onlines", [])
