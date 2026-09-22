from typing import Dict, Any, List
from urllib.parse import urlencode, quote

class Links:
    """Генерация и парсинг ссылок для подключения"""
    
    def __init__(self, panel):
        self.panel = panel

    def build_vless(self, uuid: str, host: str, port: int, 
                    params: Dict[str, str]) -> str:
        """собрать vless:// ссылку"""
        query = urlencode(params)
        return f"vless://{uuid}@{host}:{port}?{query}"

    def build_vmess(self, config: Dict[str, Any]) -> str:
        """собрать vmess:// ссылку (base64 JSON)"""
        import base64, json
        raw = json.dumps(config, separators=(",", ":"))
        return f"vmess://{base64.b64encode(raw.encode()).decode()}"

    def build_trojan(self, password: str, host: str, port: int, 
                     params: Dict[str, str]) -> str:
        """собрать trojan:// ссылку"""
        query = urlencode(params)
        return f"trojan://{password}@{host}:{port}?{query}"

    def parse(self, uri: str) -> Dict[str, Any]:
        """разобрать ссылку в словарь (protocol, host, port, params)"""
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(uri)
        return {
            "protocol": parsed.scheme,
            "host": parsed.hostname,
            "port": parsed.port,
            "params": {k: v[0] for k, v in parse_qs(parsed.query).items()},
        }

    def all(self) -> List[str]:
        """все ссылки со всех inbounds (экспорт)"""
        data = self.panel._request("GET", "panel/api/inbounds/allLinks")
        return data if isinstance(data, list) else data.get("links", [])
