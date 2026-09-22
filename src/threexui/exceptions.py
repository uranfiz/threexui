class ThreeXuiError(Exception):
    """базовая ошибка библиотеки"""
    pass

class AuthError(ThreeXuiError):
    """ошибка аутентификации"""
    pass

class APIError(ThreeXuiError):
    """панель вернула success: false"""
    def __init__(self, message: str, response: dict = None):
        super().__init__(message)
        self.response = response or {}
