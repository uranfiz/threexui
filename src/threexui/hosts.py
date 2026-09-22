from typing import List, Dict, Any

class Hosts:
    """Управление host-группами и external links"""
    
    def __init__(self, panel):
        self.panel = panel

    def list(self) -> List[Dict[str, Any]]:
        """все host-группы"""
        return self.panel._request("GET", "panel/api/hosts/list")

    def get(self, group_id: str) -> Dict[str, Any]:
        """получить host-группу по ID"""
        return self.panel._request("GET", f"panel/api/hosts/get/{group_id}")

    def by_inbound(self, inbound_id: int) -> List[Dict[str, Any]]:
        """host-группы, привязанные к inbound"""
        return self.panel._request("GET", f"panel/api/hosts/inbound/{inbound_id}")

    def tags(self) -> List[str]:
        """уникальные теги host-групп"""
        return self.panel._request("GET", "panel/api/hosts/tags")

    def add(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """создать host-группу"""
        return self.panel._request("POST", "panel/api/hosts/add", json=payload)

    def update(self, group_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """обновить host-группу"""
        return self.panel._request("POST", f"panel/api/hosts/update/{group_id}", json=payload)

    def delete(self, group_id: str) -> bool:
        """удалить host-группу"""
        self.panel._request("POST", f"panel/api/hosts/delete/{group_id}")
        return True

    def set_enable(self, group_id: str, enable: bool) -> bool:
        """включить или выключить host-группу"""
        self.panel._request("POST", f"panel/api/hosts/setEnable/{group_id}", 
                           json={"enable": enable})
        return True
