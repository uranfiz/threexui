from typing import Dict, Any, List

class Xray:
    """Управление Xray-конфигом (template, outbounds, balancers)"""
    
    def __init__(self, panel):
        self.panel = panel

    def get_config(self) -> Dict[str, Any]:
        """текущий Xray-конфиг"""
        return self.panel._request("GET", "panel/api/xray/getConfigJson")

    def get_template(self) -> Dict[str, Any]:
        """сохранённый шаблон Xray (routing, outbounds, DNS)"""
        return self.panel._request("GET", "panel/api/xray/getDefaultJsonConfig")

    def update_config(self, config: Dict[str, Any]) -> bool:
        """обновить Xray-конфиг"""
        self.panel._request("POST", "panel/api/xray/update", json=config)
        return True

    def outbounds_traffic(self) -> List[Dict[str, Any]]:
        """статистика трафика по outbounds"""
        return self.panel._request("GET", "panel/api/xray/outbounds/traffic")

    def reset_outbound(self, tag: str) -> bool:
        """сбросить трафик для outbound"""
        self.panel._request("POST", f"panel/api/xray/outbounds/reset/{tag}")
        return True

    def test_outbound(self, outbound: Dict[str, Any]) -> Dict[str, Any]:
        """проверить подключение через outbound"""
        return self.panel._request("POST", "panel/api/xray/testOutbound", json=outbound)

    def balancers(self) -> List[Dict[str, Any]]:
        """список активных балансировщиков в Xray"""
        return self.panel._request("GET", "panel/api/xray/balancers")

    def set_balancer_override(self, tag: str, target: str) -> bool:
        """привязать балансировщик к конкретному outbound"""
        self.panel._request("POST", f"panel/api/xray/balancers/{tag}/override", 
                           json={"target": target})
        return True
