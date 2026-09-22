from typing import List, Optional, Dict, Any
from .models import Inbound

class Inbounds:
    """Управление входящими подключениями (inbounds)"""
    
    def __init__(self, panel):
        self.panel = panel

    def list(self) -> List[Inbound]:
        """список всех inbounds с полными настройками"""
        data = self.panel._request("GET", "panel/api/inbounds/list")
        return [Inbound.model_validate(i) for i in data]

    def list_slim(self) -> List[Dict[str, Any]]:
        """облегчённый список (id, remark, protocol, port) для выпадающих меню"""
        return self.panel._request("GET", "panel/api/inbounds/list/slim")

    def get(self, inbound_id: int) -> Inbound:
        """получить конкретный inbound по ID"""
        data = self.panel._request("GET", f"panel/api/inbounds/get/{inbound_id}")
        return Inbound.model_validate(data)

    def add(self, payload: Dict[str, Any]) -> Inbound:
        """создать новый inbound"""
        data = self.panel._request("POST", "panel/api/inbounds/add", json=payload)
        return Inbound.model_validate(data)

    def update(self, inbound_id: int, payload: Dict[str, Any]) -> Inbound:
        """обновить inbound"""
        data = self.panel._request("POST", f"panel/api/inbounds/update/{inbound_id}", json=payload)
        return Inbound.model_validate(data)

    def delete(self, inbound_id: int) -> bool:
        """удалить inbound"""
        self.panel._request("POST", f"panel/api/inbounds/del/{inbound_id}")
        return True

    def set_enable(self, inbound_id: int, enable: bool) -> bool:
        """включить или выключить inbound"""
        self.panel._request("POST", f"panel/api/inbounds/setEnable/{inbound_id}", 
                           json={"enable": enable})
        return True

    def reset_traffic(self, inbound_id: int) -> bool:
        """сбросить счётчик трафика для inbound"""
        self.panel._request("POST", f"panel/api/inbounds/resetTraffic/{inbound_id}")
        return True
