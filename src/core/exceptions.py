"""
Excepciones personalizadas del bot template.
"""


class BotException(Exception):
    """Excepción base para el bot"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ConfigurationError(BotException):
    """Errores de configuración"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class ClientNotFoundError(BotException):
    """Cliente no encontrado"""
    def __init__(self, client_id: str):
        super().__init__(
            f"Client '{client_id}' not found",
            status_code=404
        )


class FeatureNotAvailableError(BotException):
    """Feature no disponible para el plan del cliente"""
    def __init__(self, feature_name: str, plan: str):
        super().__init__(
            f"Feature '{feature_name}' not available for plan '{plan}'",
            status_code=403
        )


class FeatureNotEnabledError(BotException):
    """Feature no habilitada para el cliente"""
    def __init__(self, feature_name: str):
        super().__init__(
            f"Feature '{feature_name}' is not enabled",
            status_code=403
        )


class TwilioError(BotException):
    """Errores relacionados con Twilio"""
    def __init__(self, message: str):
        super().__init__(f"Twilio error: {message}", status_code=502)


class AIServiceError(BotException):
    """Errores del servicio de IA"""
    def __init__(self, message: str, provider: str = "AI"):
        super().__init__(
            f"{provider} service error: {message}",
            status_code=502
        )


class RateLimitError(BotException):
    """Rate limit excedido"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status_code=429)


class DatabaseError(BotException):
    """Errores de base de datos"""
    def __init__(self, message: str):
        super().__init__(f"Database error: {message}", status_code=500)


class ValidationError(BotException):
    """Errores de validación"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)
