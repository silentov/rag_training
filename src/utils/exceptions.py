class LLMBusinessException(Exception):
    """Базовый класс для исключений LLM-сервиса"""

    def __init__(self, message: str, status_code: int, rquid: str | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.request_rquid = rquid


class TokenLimitExceededError(LLMBusinessException):
    def __init__(self, tokens: int):
        super().__init__(f"Превышен лимит токенов: {tokens}", 413)


class RateLimitError(LLMBusinessException):
    def __init__(self, rquid: str):
        super().__init__("Слишком много запросов", 429, rquid)


class BackendError(LLMBusinessException):
    def __init__(self, code: int):
        super().__init__("Ошибка сервера GigaChat", code)
