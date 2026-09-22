from typing import Dict, Any

class Generators:
    """Серверные генераторы ключей и сертификатов"""
    
    def __init__(self, panel):
        self.panel = panel

    def uuid(self) -> str:
        """сгенерировать новый UUID"""
        data = self.panel._request("POST", "panel/api/server/getNewUUID")
        return data.get("uuid", data) if isinstance(data, dict) else data

    def x25519(self) -> Dict[str, str]:
        """сгенерировать пару ключей X25519 (Reality)"""
        return self.panel._request("POST", "panel/api/server/getNewX25519Cert")

    def mldsa65(self) -> Dict[str, str]:
        """сгенерировать ML-DSA-65 ключи"""
        return self.panel._request("POST", "panel/api/server/getNewmldsa65")

    def mlkem768(self) -> Dict[str, str]:
        """сгенерировать ML-KEM-768 ключи"""
        return self.panel._request("POST", "panel/api/server/getNewmlkem768")

    def ech_cert(self, sni: str) -> Dict[str, str]:
        """сгенерировать ECH-сертификат для указанного SNI"""
        return self.panel._request("POST", "panel/api/server/getNewEchCert", 
                                  json={"sni": sni})

    def vless_enc(self) -> Dict[str, str]:
        """сгенерировать настройки шифрования VLESS"""
        return self.panel._request("POST", "panel/api/server/getNewVlessEnc")
