from typing import Optional, Dict, Any

class Subscriptions:
    """Работа с подписками (Sub Links)"""
    
    def __init__(self, panel):
        self.panel = panel

    def get_raw(self, sub_id: str) -> str:
        """получить base64-список ссылок для подписки"""
        data = self.panel._request("GET", f"panel/api/clients/subLinks/{sub_id}")
        return data if isinstance(data, str) else data.get("link", "")

    def get_json(self, sub_id: str) -> Dict[str, Any]:
        """получить JSON-конфиг подписки (для Xray)"""
        return self.panel._request("GET", f"panel/api/clients/subJson/{sub_id}")

    def get_clash(self, sub_id: str) -> str:
        """получить YAML-конфиг подписки (для Clash/Mihomo)"""
        return self.panel._request("GET", f"panel/api/clients/subClash/{sub_id}")

    def link(self, sub_id: str, base_url: Optional[str] = None) -> str:
        """собрать готовую subscription-ссылку"""
        base = base_url or self.panel.base_url
        return f"{base}/sub/{sub_id}"
