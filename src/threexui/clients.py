from typing import List, Optional, Union, Dict, Any
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

    def list(self) -> List[Client]:
        """получить всех клиентов"""
        data = self.panel._request("GET", "panel/api/clients/list")
        return [Client.model_validate(c) for c in data]

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

    def update(self, email: str, **fields) -> Client:
        """обновить поля клиента"""
        if "total_gb" in fields:
            fields["totalGB"] = self._traffic_to_bytes(fields.pop("total_gb"))
        if "expires" in fields:
            fields["expiryTime"] = self._expiry_to_ms(fields.pop("expires"))

        data = self.panel._request("POST", f"panel/api/clients/update/{email}", json=fields)
        return Client.model_validate(data)

    def delete(self, email: str, keep_traffic: bool = False):
        """удалить клиента. keep_traffic=True оставит записи статистики."""
        params = {"keepTraffic": "true" if keep_traffic else "false"}
        return self.panel._request("DELETE", f"panel/api/clients/del/{email}", params=params)

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

    def online(self) -> List[str]:
        """список email'ов, которые сейчас онлайн"""
        data = self.panel._request("GET", "panel/api/clients/onlines")
        return data if isinstance(data, list) else data.get("onlines", [])

    def ips(self, email: str) -> List[str]:
        """получить список IP-адресов, с которых подключался клиент"""
        data = self.panel._request("GET", f"panel/api/clients/ips/{email}")
        return data if isinstance(data, list) else data.get("ips", [])

    def clear_ips(self, email: str):
        """очистить список IP клиента"""
        return self.panel._request("POST", f"panel/api/clients/clearIps/{email}")

    def extend(self, emails: List[str], days: int = 0, gigabytes: int = 0):
        """продлить клиентам время и/или добавить трафик.

        Args:
            emails: список email клиентов
            days: на сколько дней продлить (может быть отрицательным)
            gigabytes: сколько ГБ добавить (может быть отрицательным)
        """
        payload = {
            "emails": emails,
            "days": days,
            "gigabytes": gigabytes,
        }
        return self.panel._request("POST", "panel/api/clients/extend", json=payload)

    def bulk_add(self, clients: List[Dict[str, Any]]) -> List[Client]:
        """массово создать клиентов.

        Каждый элемент списка должен содержать: email, inbound_ids, total_gb, expires
        """
        results = []
        for c in clients:
            result = self.add(
                email=c["email"],
                inbound_ids=c["inbound_ids"],
                total_gb=c.get("total_gb"),
                expires=c.get("expires"),
                limit_ip=c.get("limit_ip", 0),
            )
            results.append(result)
        return results

    def bulk_delete(self, emails: List[str], keep_traffic: bool = False):
        """массово удалить клиентов"""
        for email in emails:
            self.delete(email, keep_traffic=keep_traffic)

    def bulk_enable(self, emails: List[str]):
        """массово включить клиентов"""
        for email in emails:
            self.update(email, enable=True)

    def bulk_disable(self, emails: List[str]):
        """массово выключить клиентов"""
        for email in emails:
            self.update(email, enable=False)

    def bulk_reset_traffic(self, emails: List[str]):
        """массово сбросить трафик"""
        for email in emails:
            self.reset_traffic(email)

    def delete_depleted(self) -> int:
        """удалить всех клиентов с истёкшим трафиком или сроком. Возвращает количество удалённых"""
        data = self.panel._request("POST", "panel/api/clients/delDepleted")
        return data.get("deleted", 0) if isinstance(data, dict) else 0

    def attach(self, email: str, inbound_ids: List[int]):
        """привязать клиента к дополнительным inbounds"""
        return self.panel._request("POST", f"panel/api/clients/attach/{email}", json={"inboundIds": inbound_ids})

    def detach(self, email: str, inbound_ids: List[int]):
        """отвязать клиента от inbounds"""
        return self.panel._request("POST", f"panel/api/clients/detach/{email}", json={"inboundIds": inbound_ids})
