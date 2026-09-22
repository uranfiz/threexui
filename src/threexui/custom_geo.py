from typing import List, Dict, Any

class CustomGeo:
    """Управление кастомными geo-списками (geosite/geoip)"""
    
    def __init__(self, panel):
        self.panel = panel

    def list(self) -> List[Dict[str, Any]]:
        """список всех кастомных geo-записей"""
        return self.panel._request("GET", "panel/api/custom-geo/list")

    def aliases(self) -> Dict[str, Any]:
        """получить алиасы для встроенных geo-файлов"""
        return self.panel._request("GET", "panel/api/custom-geo/aliases")

    def add(self, geo_type: str, alias: str, url: str) -> Dict[str, Any]:
        """добавить кастомный geo-файл"""
        return self.panel._request("POST", "panel/api/custom-geo/add", 
                                   json={"type": geo_type, "alias": alias, "url": url})

    def update(self, geo_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """обновить geo-запись"""
        return self.panel._request("POST", f"panel/api/custom-geo/update/{geo_id}", json=payload)

    def delete(self, geo_id: int) -> bool:
        """удалить geo-запись"""
        self.panel._request("POST", f"panel/api/custom-geo/delete/{geo_id}")
        return True

    def download(self, geo_id: int) -> bool:
        """скачать geo-файл"""
        self.panel._request("POST", f"panel/api/custom-geo/download/{geo_id}")
        return True

    def update_all(self) -> Dict[str, Any]:
        """обновить все кастомные geo-файлы"""
        return self.panel._request("POST", "panel/api/custom-geo/update-all")
