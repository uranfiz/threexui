from typing import Dict, Any, List

class Settings:
    """Управление настройками панели (Subscription, Security, Telegram)"""
    
    def __init__(self, panel):
        self.panel = panel

    def get_all(self) -> Dict[str, Any]:
        """получить все настройки панели"""
        return self.panel._request("POST", "panel/setting/all")

    def get_default(self) -> Dict[str, Any]:
        """получить настройки по умолчанию"""
        return self.panel._request("POST", "panel/setting/defaultSettings")

    def update(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """обновить настройки панели (sub, security, telegram и тд)"""
        return self.panel._request("POST", "panel/setting/update", json=settings)

    def update_user(self, old_username: str, old_password: str, 
                    new_username: str, new_password: str) -> bool:
        """сменить логин и пароль администратора"""
        payload = {
            "oldUsername": old_username,
            "oldPassword": old_password,
            "newUsername": new_username,
            "newPassword": new_password,
        }
        self.panel._request("POST", "panel/setting/updateUser", json=payload)
        return True

    def restart_panel(self) -> bool:
        """перезапустить панель"""
        self.panel._request("POST", "panel/setting/restartPanel")
        return True
