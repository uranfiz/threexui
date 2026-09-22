from datetime import datetime, timedelta

def bytes_to_gb(n: int) -> float:
    """байты в гигабайты"""
    return n / (1024 ** 3)

def gb_to_bytes(n: float) -> int:
    """гигабайты в байты"""
    return int(n * (1024 ** 3))

def ms_to_datetime(ms: int) -> datetime:
    """Unix-миллисекунды в datetime"""
    return datetime.fromtimestamp(ms / 1000)

def datetime_to_ms(dt: datetime) -> int:
    """datetime в Unix-миллисекунды"""
    return int(dt.timestamp() * 1000)

def days_to_ms(days: int) -> int:
    """дни в Unix-миллисекунды"""
    return int((datetime.now() + timedelta(days=days)).timestamp() * 1000)
