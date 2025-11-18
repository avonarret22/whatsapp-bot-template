"""
Gestión del contexto del cliente actual.
Utiliza ContextVar para ser thread-safe en entornos async.
"""
from contextvars import ContextVar
from typing import Optional
from src.core.config import ClientConfig

# Context variable para el cliente actual (thread-safe para async)
_current_client: ContextVar[Optional[ClientConfig]] = ContextVar(
    'current_client',
    default=None
)

_current_feature_manager: ContextVar[Optional[Any]] = ContextVar(
    'current_feature_manager',
    default=None
)


class ClientContext:
    """
    Gestiona el contexto del cliente actual en cada request.

    Cada request HTTP puede ser para un cliente diferente,
    por lo que usamos ContextVar para mantener aislamiento.
    """

    @staticmethod
    def set(client_config: ClientConfig):
        """
        Establece el cliente actual para el contexto de ejecución.

        Args:
            client_config: Configuración del cliente
        """
        _current_client.set(client_config)

    @staticmethod
    def get() -> ClientConfig:
        """
        Obtiene el cliente actual del contexto.

        Returns:
            Configuración del cliente actual

        Raises:
            RuntimeError: Si no hay cliente en el contexto
        """
        client = _current_client.get()
        if client is None:
            raise RuntimeError(
                "No client context set. "
                "Make sure ClientResolverMiddleware is configured."
            )
        return client

    @staticmethod
    def get_safe() -> Optional[ClientConfig]:
        """
        Obtiene el cliente actual sin lanzar excepción.

        Returns:
            Configuración del cliente o None si no está configurado
        """
        return _current_client.get()

    @staticmethod
    def clear():
        """Limpia el contexto del cliente"""
        _current_client.set(None)

    @staticmethod
    def set_feature_manager(feature_manager):
        """Establece el feature manager del cliente actual"""
        _current_feature_manager.set(feature_manager)

    @staticmethod
    def get_feature_manager():
        """Obtiene el feature manager del cliente actual"""
        manager = _current_feature_manager.get()
        if manager is None:
            raise RuntimeError("No feature manager set in context")
        return manager

    @staticmethod
    def clear_feature_manager():
        """Limpia el feature manager del contexto"""
        _current_feature_manager.set(None)


# Funciones de conveniencia
def get_current_client() -> ClientConfig:
    """Shortcut para obtener el cliente actual"""
    return ClientContext.get()


def get_current_client_safe() -> Optional[ClientConfig]:
    """Shortcut para obtener el cliente actual (safe)"""
    return ClientContext.get_safe()
