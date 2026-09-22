from typing import List, Optional, Dict, Any

class Nodes:
    """Управление нодами (multi-node cluster)"""
    
    def __init__(self, panel):
        self.panel = panel

    def list(self) -> List[Dict[str, Any]]:
        """список всех нод"""
        return self.panel._request("GET", "panel/api/nodes/list")

    def get(self, node_id: int) -> Dict[str, Any]:
        """получить конкретную ноду по ID"""
        return self.panel._request("GET", f"panel/api/nodes/get/{node_id}")

    def history(self, node_id: int, metric: str = "cpu", bucket: int = 60) -> List[Dict]:
        """история метрик ноды (cpu, memory, и тд)"""
        return self.panel._request("GET", f"panel/api/nodes/history/{node_id}/{metric}/{bucket}")

    def add(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """добавить новую ноду"""
        return self.panel._request("POST", "panel/api/nodes/add", json=payload)

    def update(self, node_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """обновить ноду"""
        return self.panel._request("POST", f"panel/api/nodes/update/{node_id}", json=payload)

    def delete(self, node_id: int) -> bool:
        """удалить ноду"""
        self.panel._request("POST", f"panel/api/nodes/del/{node_id}")
        return True

    def set_enable(self, node_id: int, enable: bool) -> bool:
        """включить или выключить ноду"""
        self.panel._request("POST", f"panel/api/nodes/setEnable/{node_id}", 
                           json={"enable": enable})
        return True

    def test(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """проверить подключение к ноде с указанными данными"""
        return self.panel._request("POST", "panel/api/nodes/test", json=node_data)

    def probe(self, node_id: int) -> Dict[str, Any]:
        """проверить статус конкретной ноды"""
        return self.panel._request("POST", f"panel/api/nodes/probe/{node_id}")
