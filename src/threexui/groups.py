from typing import List, Dict, Any

class Groups:
    """Управление группами клиентов (client groups)"""
    
    def __init__(self, panel):
        self.panel = panel

    def list(self) -> List[Dict[str, Any]]:
        """список всех групп"""
        return self.panel._request("GET", "panel/api/clients/groups/list")

    def get_emails(self, group_name: str) -> List[str]:
        """получить список email'ов клиентов в группе"""
        data = self.panel._request("GET", f"panel/api/clients/groups/{group_name}/emails")
        return data if isinstance(data, list) else data.get("emails", [])

    def create(self, name: str) -> bool:
        """создать новую группу"""
        self.panel._request("POST", "panel/api/clients/groups/create", json={"name": name})
        return True

    def rename(self, old_name: str, new_name: str) -> bool:
        """переименовать группу"""
        self.panel._request("POST", "panel/api/clients/groups/rename", 
                           json={"oldName": old_name, "newName": new_name})
        return True

    def delete(self, name: str) -> bool:
        """удалить группу"""
        self.panel._request("POST", "panel/api/clients/groups/delete", json={"name": name})
        return True

    def bulk_add(self, emails: List[str], group: str) -> bool:
        """массово добавить клиентов в группу"""
        self.panel._request("POST", "panel/api/clients/groups/bulkAdd", 
                           json={"emails": emails, "group": group})
        return True

    def bulk_remove(self, emails: List[str]) -> bool:
        """массово удалить клиентов из их текущих групп"""
        self.panel._request("POST", "panel/api/clients/groups/bulkRemove", 
                           json={"emails": emails})
        return True
