"""
Proveedor de Google Gemini para generación de respuestas.
"""
from typing import Dict, Any, List
import google.generativeai as genai
from src.features.ai_responses.providers.base_provider import AIProvider
from src.core.exceptions import AIServiceError
import logging

logger = logging.getLogger(__name__)


class GeminiProvider(AIProvider):
    """Implementación de AIProvider usando Google Gemini"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)

        # Configurar Gemini
        api_key = config.get('api_key')
        if not api_key:
            raise ValueError("Gemini API key not provided")

        genai.configure(api_key=api_key)

        # Parámetros del modelo
        self.model_name = config.get('model', 'gemini-1.5-flash')
        self.temperature = config.get('temperature', 0.8)
        self.max_tokens = config.get('max_tokens', 500)

        # Crear modelo
        self.model = genai.GenerativeModel(self.model_name)

        logger.info(f"Gemini provider initialized: {self.model_name}")

    async def generate_response(
        self,
        message: str,
        system_prompt: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Genera respuesta usando Gemini.

        Args:
            message: Mensaje del usuario
            system_prompt: Instrucciones del sistema
            conversation_history: Historial (opcional)

        Returns:
            Respuesta generada
        """
        try:
            # Construir prompt completo
            full_prompt = f"{system_prompt}\n\nUsuario: {message}\nAsistente:"

            # Si hay historial, incluirlo
            if conversation_history:
                history_text = "\n".join([
                    f"{msg['role']}: {msg['content']}"
                    for msg in conversation_history[-5:]  # Últimos 5 mensajes
                ])
                full_prompt = f"{system_prompt}\n\nHistorial:\n{history_text}\n\nUsuario: {message}\nAsistente:"

            # Generar respuesta
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                )
            )

            if not response or not response.text:
                raise AIServiceError("Empty response from Gemini", "Gemini")

            return response.text.strip()

        except Exception as e:
            logger.error(f"Gemini generation error: {e}", exc_info=True)
            raise AIServiceError(str(e), "Gemini")

    def get_name(self) -> str:
        return f"Gemini ({self.model_name})"

    def cleanup(self):
        """No hay recursos específicos que limpiar con Gemini"""
        logger.info("Gemini provider cleaned up")
