"""
Proveedor base de IA (interface).
Diferentes providers (Gemini, Claude, OpenAI) implementan esta interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List


class AIProvider(ABC):
    """Interface para proveedores de IA"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def generate_response(
        self,
        message: str,
        system_prompt: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Genera una respuesta usando el modelo de IA.

        Args:
            message: Mensaje del usuario
            system_prompt: Prompt de sistema con personalidad
            conversation_history: Historial de conversación

        Returns:
            Respuesta generada por la IA
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Retorna el nombre del provider"""
        pass

    @abstractmethod
    def cleanup(self):
        """Limpia recursos del provider"""
        pass
