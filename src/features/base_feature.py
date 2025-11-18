"""
Clase base abstracta para todas las features del bot.
Todas las features deben heredar de esta clase.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from fastapi import APIRouter


class BaseFeature(ABC):
    """
    Clase base abstracta para features del bot.

    Cada feature debe implementar:
    - initialize(): Setup de la feature
    - cleanup(): Limpieza de recursos
    - get_routes(): Rutas FastAPI (opcional)
    - process_message(): Procesar mensajes
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Constructor base.

        Args:
            config: Configuración de la feature desde el YAML del cliente
        """
        self.config = config
        self.enabled = config.get('enabled', False)

    @abstractmethod
    def initialize(self):
        """
        Inicializa la feature.
        Aquí se cargan recursos, conexiones, modelos, etc.

        Raises:
            Exception: Si falla la inicialización
        """
        pass

    @abstractmethod
    def cleanup(self):
        """
        Limpia recursos cuando se desactiva la feature.
        Cierra conexiones, libera memoria, etc.
        """
        pass

    @abstractmethod
    def get_routes(self) -> Optional[APIRouter]:
        """
        Retorna las rutas FastAPI de la feature (si tiene).

        Returns:
            APIRouter con las rutas o None si no tiene rutas
        """
        pass

    @abstractmethod
    async def process_message(
        self,
        message: str,
        user_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Procesa un mensaje de usuario.

        Args:
            message: Mensaje del usuario
            user_context: Contexto del usuario (historial, config, etc.)

        Returns:
            Dict con la respuesta procesada, o None si esta feature no aplica

        Ejemplo de retorno:
        {
            "response": "Texto de respuesta",
            "metadata": {
                "provider": "gemini",
                "tokens": 123
            }
        }
        """
        pass

    def get_name(self) -> str:
        """Retorna el nombre de la feature"""
        return self.__class__.__name__

    def is_enabled(self) -> bool:
        """Verifica si la feature está habilitada"""
        return self.enabled

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración.

        Args:
            key: Clave de configuración
            default: Valor por defecto si no existe

        Returns:
            Valor de configuración o default
        """
        return self.config.get(key, default)
