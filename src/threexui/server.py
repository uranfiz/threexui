from typing import List, Optional, Dict, Any

class Server:
    """Статус и управление сервером/панелью"""
    
    def __init__(self, panel):
        self.panel = panel

    def status(self) -> Dict[str, Any]:
        """статус сервера: CPU, RAM, Disk, Xray state"""
        return self.panel._request("GET", "panel/api/server/status")

    def cpu_history(self, bucket: int = 60) -> List[Dict]:
        """история загрузки CPU"""
        return self.panel._request("GET", f"panel/api/server/cpuHistory/{bucket}")

    def xray_versions(self) -> List[str]:
        """доступные версии Xray для установки"""
        return self.panel._request("GET", "panel/api/server/getXrayVersion")

    def config_json(self) -> str:
        """текущий конфиг Xray в JSON"""
        return self.panel._request("GET", "panel/api/server/getConfigJson")

    def restart_xray(self) -> bool:
        """перезапустить Xray"""
        self.panel._request("POST", "panel/api/server/restartXray")
        return True

    def stop_xray(self) -> bool:
        """остановить Xray"""
        self.panel._request("POST", "panel/api/server/stopXray")
        return True

    def install_xray(self, version: str) -> bool:
        """установить конкретную версию Xray"""
        self.panel._request("POST", "panel/api/server/installXray", 
                           json={"version": version})
        return True

    def logs(self, count: int = 100) -> List[str]:
        """получить логи панели"""
        data = self.panel._request("GET", f"panel/api/server/logs/{count}")
        return data if isinstance(data, list) else data.get("logs", [])

    def xray_logs(self, count: int = 100) -> List[str]:
        """получить логи Xray"""
        data = self.panel._request("GET", f"panel/api/server/xraylogs/{count}")
        return data if isinstance(data, list) else data.get("logs", [])
