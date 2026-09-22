# threexui

> Удобная Python-библиотека для управления панелью [3x-ui](https://github.com/MHSanaei/3x-ui).

[![PyPI version](https://img.shields.io/pypi/v/threexui.svg)](https://pypi.org/project/threexui/)
[![Python versions](https://img.shields.io/pypi/pyversions/threexui.svg)](https://pypi.org/project/threexui/)
[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/telegram-@devuranium-blue.svg)](https://t.me/devuranium)

**threexui** — обёртка над REST API панели 3x-ui. Позволяет управлять inbounds, клиентами, подписками, нодами и Xray-конфигом из Python. Вместо десятков HTTP-запросов вручную — одна строка кода.

Создана для автоматизации выдачи VPN-доступов, массового импорта клиентов, генерации ссылок и построения дашбордов.

---

## Оглавление

- [Установка](#установка)
- [Быстрый старт](#быстрый-старт)
- [API](#api)
  - [Panel](#panel)
  - [Clients](#clients)
  - [Inbounds](#inbounds)
  - [Groups](#groups)
  - [Nodes](#nodes)
  - [Server](#server)
  - [Generators](#generators)
  - [Settings](#settings)
  - [Subscriptions](#subscriptions)
  - [Links](#links)
  - [CustomGeo](#customgeo)
  - [Xray](#xray)
  - [Hosts](#hosts)
- [Обработка ошибок](#обработка-ошибок)
- [Требования](#требования)
- [Лицензия](#лицензия)

---

## Установка

```bash
pip install threexui
```

**Требования:** Python 3.10+, панель 3x-ui версии 2.x или выше.

---

## Быстрый старт

```python
from threexui import Panel
from datetime import timedelta

# подключение по API-токену (рекомендуется)
panel = Panel("https://panel.example.com:2053", token="YOUR_API_TOKEN")

# или по логину/паролю
panel = Panel("https://panel.example.com:2053")
panel.login("admin", "password")

# создать клиента на 30 дней, 100 ГБ, привязать к inbounds [3, 5]
panel.clients.add(
    email="user123",
    inbound_ids=[3, 5],
    total_gb=100,
    expires=timedelta(days=30),
    limit_ip=2,
)

# получить все ссылки для клиента
for link in panel.clients.links("user123"):
    print(link)

# получить subscription-ссылку
client = panel.clients.get("user123")
print(panel.subscriptions.link(client.sub_id))
```

---

## API

### Panel

Главный класс. Создаётся один раз и держит сессию.

```python
from threexui import Panel

panel = Panel(
    base_url="https://panel.example.com:2053",
    token="YOUR_API_TOKEN",       # опционально
    username="admin",             # опционально
    password="password",          # опционально
    verify_ssl=True,              # отключи, если самоподписанный сертификат
)

# авторизация по логину/паролю
panel.login("admin", "password")
panel.login("admin", "password", two_factor_code="123456")  # с 2FA

# контекстный менеджер
with Panel("https://panel.example.com:2053", token="...") as panel:
    print(panel.clients.links("user123"))
```

---

### Clients

Управление клиентами: создание, обновление, удаление, ссылки, трафик, массовые операции.

```python
# все клиенты
for client in panel.clients.list():
    used = client.traffic.up + client.traffic.down
    print(client.email, used, client.enable)

# создать клиента
panel.clients.add(
    email="user123",
    inbound_ids=[3, 5],
    total_gb=100,                 # лимит трафика, None = безлимит
    expires=timedelta(days=30),   # timedelta или datetime, None = бессрочно
    limit_ip=2,
)

# получить клиента
client = panel.clients.get("user123")
print(client.email, client.enable, client.total_gb)

# все ссылки (vless://, vmess://, trojan://)
links = panel.clients.links("user123")

# подписка
sub_link = panel.clients.sub_links(client.sub_id)

# трафик
traffic = panel.clients.traffic("user123")
print(f"↓{traffic.down / 1024**3:.2f} GB / ↑{traffic.up / 1024**3:.2f} GB")

# сбросить трафик
panel.clients.reset_traffic("user123")

# обновить поля
panel.clients.update("user123", total_gb=200, enable=False)

# удалить
panel.clients.delete("user123")
panel.clients.delete("user123", keep_traffic=True)  # оставить статистику

# кто онлайн
online = panel.clients.online()

# IP-адреса клиента
ips = panel.clients.ips("user123")
panel.clients.clear_ips("user123")

# продлить и пополнить
panel.clients.extend(["alice", "bob"], days=30, gigabytes=100)

# привязать/отвязать inbounds
panel.clients.attach("user123", [5, 7])
panel.clients.detach("user123", [3])
```

**Массовые операции:**

```python
# создать пачку клиентов
panel.clients.bulk_add([
    {"email": "user1", "inbound_ids": [3], "total_gb": 50, "expires": timedelta(days=30)},
    {"email": "user2", "inbound_ids": [3], "total_gb": 100, "expires": timedelta(days=60)},
])

# массовое удаление
panel.clients.bulk_delete(["user1", "user2"])

# массово включить/выключить
panel.clients.bulk_enable(["user1", "user2"])
panel.clients.bulk_disable(["user3", "user4"])

# массово сбросить трафик
panel.clients.bulk_reset_traffic(["user1", "user2"])

# удалить всех с истёкшим трафиком/сроком
deleted = panel.clients.delete_depleted()
print(f"Удалено: {deleted}")
```

---

### Inbounds

Управление входящими подключениями.

```python
# список всех inbounds
inbounds = panel.inbounds.list()
for i in inbounds:
    print(i.id, i.remark, i.protocol, i.port)

# облегчённый список для меню
slim = panel.inbounds.list_slim()

# конкретный inbound
inbound = panel.inbounds.get(3)

# создать
panel.inbounds.add({
    "remark": "VLESS Reality",
    "protocol": "vless",
    "port": 443,
    "settings": "{}",
    "streamSettings": "{}",
})

# обновить
panel.inbounds.update(3, {"port": 8443})

# включить/выключить
panel.inbounds.set_enable(3, False)

# сбросить трафик
panel.inbounds.reset_traffic(3)

# удалить
panel.inbounds.delete(3)
```

---

### Groups

Группы клиентов — удобно для тарифов (trial, premium).

```python
# список групп
groups = panel.groups.list()

# Email'ы в группе
emails = panel.groups.get_emails("premium")

# создать
panel.groups.create("trial")

# переименовать
panel.groups.rename("trial", "basic")

# массово добавить в группу
panel.groups.bulk_add(["user1", "user2", "user3"], "premium")

# массово убрать из групп
panel.groups.bulk_remove(["user1", "user2"])

# удалить группу
panel.groups.delete("basic")
```

---

### Nodes

Мульти-нода (если у тебя кластер из нескольких серверов).

```python
# список нод
nodes = panel.nodes.list()

# конкретная нода
node = panel.nodes.get(1)

# добавить ноду
panel.nodes.add({
    "name": "Singapore",
    "address": "sg.example.com",
    "port": 2053,
    "apiToken": "...",
})

# проверить подключение
panel.nodes.test({"address": "sg.example.com", "port": 2053, "apiToken": "..."})

# проверить статус
status = panel.nodes.probe(1)

# история метрик (cpu, mem, traffic)
history = panel.nodes.history(1, metric="cpu", bucket=60)

# включить/выключить
panel.nodes.set_enable(1, True)

# удалить
panel.nodes.delete(1)
```

---

### Server

Статус и управление сервером.

```python
# статус (CPU, RAM, Disk, Xray state)
print(panel.server.status())

# история CPU
panel.server.cpu_history(bucket=60)

# логи
panel.server.logs(count=100)
panel.server.xray_logs(count=100)

# рестарт Xray
panel.server.restart_xray()
panel.server.stop_xray()

# доступные версии Xray
versions = panel.server.xray_versions()
panel.server.install_xray(version="25.9.11")
```

---

### Generators

Серверные генераторы ключей. Не надо тащить crypto-библиотеки.

```python
# UUID
uuid = panel.generators.uuid()

# X25519 (Reality)
keys = panel.generators.x25519()
print(keys["privateKey"], keys["publicKey"])

# пост-квантовые ключи
panel.generators.mldsa65()
panel.generators.mlkem768()

# ECH-сертификат для SNI
panel.generators.ech_cert("microsoft.com")

# VLESS encryption
panel.generators.vless_enc()
```

---

### Settings

Настройки панели.

```python
# все настройки
panel.settings.get_all()

# обновить (sub, security, telegram)
panel.settings.update({
    "subEnable": True,
    "subPort": 2096,
    "subPath": "/sub/",
})

# сменить логин/пароль админа
panel.settings.update_user("admin", "oldpass", "newadmin", "newpass")

# перезапустить панель
panel.settings.restart_panel()
```

---

### Subscriptions

Работа с подписками.

```python
sub_id = "abcd1234"

# Base64-список ссылок
raw = panel.subscriptions.get_raw(sub_id)

# JSON-конфиг (для Xray)
json_config = panel.subscriptions.get_json(sub_id)

# YAML для Clash/Mihomo
clash = panel.subscriptions.get_clash(sub_id)

# готовая subscription-ссылка
print(panel.subscriptions.link(sub_id))
```

---

### Links

Сборка и парсинг ссылок вручную.

```python
# VLESS
link = panel.links.build_vless(
    uuid="...",
    host="1.2.3.4",
    port=443,
    params={"type": "tcp", "security": "reality", "sni": "microsoft.com"},
)

# VMess
link = panel.links.build_vmess({
    "v": "2", "ps": "MyServer", "add": "1.2.3.4", "port": "443",
    "id": "uuid", "aid": "0", "net": "tcp", "type": "none",
})

# Trojan
link = panel.links.build_trojan(
    password="pass",
    host="1.2.3.4",
    port=443,
    params={"sni": "example.com"},
)

# парсинг
info = panel.links.parse("vless://uuid@1.2.3.4:443?type=tcp")
print(info["protocol"], info["host"], info["port"])

# все ссылки со всех inbounds
all_links = panel.links.all()
```

---

### CustomGeo

Кастомные geo-списки (geosite / geoip).

```python
# список
panel.custom_geo.list()

# алиасы
panel.custom_geo.aliases()

# добавить
panel.custom_geo.add(
    geo_type="geosite",
    alias="my-sites",
    url="https://example.com/sites.dat",
)

# скачать
panel.custom_geo.download(geo_id=1)

# обновить всё
panel.custom_geo.update_all()

# удалить
panel.custom_geo.delete(1)
```

---

### Xray

Управление Xray-конфигом и outbounds.

```python
# текущий конфиг
panel.xray.get_config()

# шаблон (routing, outbounds, DNS)
panel.xray.get_template()

# обновить конфиг
panel.xray.update_config({...})

# трафик по outbounds
panel.xray.outbounds_traffic()

# сбросить трафик
panel.xray.reset_outbound(tag="proxy")

# проверить подключение
panel.xray.test_outbound({"protocol": "freedom", "tag": "test"})

# балансировщики
panel.xray.balancers()
panel.xray.set_balancer_override(tag="balancer1", target="outbound1")
```

---

### Hosts

Host-группы и external links.

```python
# все host-группы
panel.hosts.list()

# конкретная группа
panel.hosts.get("group-id")

# host-группы для inbound
panel.hosts.by_inbound(inbound_id=3)

# теги
panel.hosts.tags()

# создать
panel.hosts.add({
    "inboundId": 3,
    "remark": "Premium",
    "address": "premium.example.com",
})

# обновить
panel.hosts.update("group-id", {"remark": "VIP"})

# включить/выключить
panel.hosts.set_enable("group-id", True)

# удалить
panel.hosts.delete("group-id")
```

---

## Обработка ошибок

```python
from threexui import Panel, ThreeXuiError, AuthError, APIError

try:
    panel = Panel("https://panel.example.com:2053", token="bad-token")
    panel.clients.links("user123")
except AuthError as e:
    print(f"Не авторизован: {e}")
except APIError as e:
    print(f"Панель вернула ошибку: {e}")
except ThreeXuiError as e:
    print(f"Ошибка библиотеки: {e}")
```

| Исключение | Когда возникает |
|------------|-----------------|
| `ThreeXuiError` | Базовая ошибка (сеть, парсинг) |
| `AuthError` | Ошибка авторизации (401) |
| `APIError` | Панель вернула `success: false` |

---

## Требования

- **Python:** 3.10+
- **3x-ui:** версия 2.x или выше
- **Зависимости:** `requests>=2.31.0`, `pydantic>=2.0.0`

---

## Лицензия

GNU Affero General Public License v3.0 (AGPL-3.0). См. [LICENSE](LICENSE).

---

## Автор

**Dream** — [@devuranium](https://t.me/devuranium)

**Бот** для обратной связи / **идей** / багов: [@libsmods_bot](https://t.me/libsmods_bot).

Issues и pull requests приветствуются на [GitHub](https://github.com/uranfiz/threexui).
