from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class ClientTraffic(BaseModel):
    up: int = 0
    down: int = 0
    total: int = 0  # 0 = безлимит
    expiry_time: int = 0  # Unix ms, 0 = безлимит

class Client(BaseModel):
    id: str
    email: str
    enable: bool = True
    total_gb: int = 0
    expiry_time: int = 0
    limit_ip: int = 0
    limit_hwid: int = 0
    sub_id: Optional[str] = None
    traffic: Optional[ClientTraffic] = None

class Inbound(BaseModel):
    id: int
    remark: str
    protocol: str
    port: int
    enable: bool = True
    settings: dict = Field(default_factory=dict)
    stream_settings: dict = Field(default_factory=dict, alias="streamSettings")
    sniffing: dict = Field(default_factory=dict)
    client_stats: List[dict] = Field(default_factory=list, alias="clientStats")
