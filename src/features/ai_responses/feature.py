"""
Feature de respuestas con IA.
Soporta múltiples providers (Gemini, Claude, OpenAI) mediante Strategy Pattern.
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter
from src.features.base_feature import BaseFeature
from src.features.ai_responses.providers.base_provider import AIProvider
from src.features.ai_responses.providers.gemini_provider import GeminiProvider
from src.core.exceptions import ConfigurationError, AIServiceError
import logging

logger = logging.getLogger(__name__)


class AIResponsesFeature(BaseFeature):
    """
    Feature principal de respuestas con IA.

    Responsabilidades:
    - Seleccionar el provider de IA (Gemini/Claude/OpenAI)
    - Generar respuestas basadas en la personalidad del bot
    - Manejar fallbacks si falla el provider principal
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.ai_provider: Optional[AIProvider] = None

    def initialize(self):
        """Inicializa el proveedor de IA según configuración"""

        provider_name = self.config.get('provider', 'gemini')
        provider_config = self.config.get('provider_config', {})

        logger.info(f"Initializing AI provider: {provider_name}")

        # Factory Pattern para seleccionar provider
        providers = {
            'gemini': GeminiProvider,
            # 'claude': ClaudeProvider,  # TODO: Implementar
            # 'openai': OpenAIProvider,  # TODO: Implementar
        }

        provider_class = providers.get(provider_name)
        if not provider_class:
            raise ConfigurationError(
                f"Unknown AI provider: {provider_name}. "
                f"Available: {list(providers.keys())}"
            )

        try:
            self.ai_provider = provider_class(provider_config)
            logger.info(f"AI provider initialized successfully: {self.ai_provider.get_name()}")

        except Exception as e:
            logger.error(f"Failed to initialize AI provider: {e}", exc_info=True)
            raise ConfigurationError(f"AI provider initialization failed: {e}")

    def cleanup(self):
        """Limpia recursos del AI provider"""
        if self.ai_provider:
            try:
                self.ai_provider.cleanup()
                logger.info("AI provider cleaned up")
            except Exception as e:
                logger.error(f"Error cleaning up AI provider: {e}")

    def get_routes(self) -> Optional[APIRouter]:
        """Esta feature no expone rutas propias"""
        return None

    async def process_message(
        self,
        message: str,
        user_context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Genera respuesta con IA basándose en el mensaje y contexto.

        Args:
            message: Mensaje del usuario
            user_context: Contexto con personalidad, historial, etc.

        Returns:
            Dict con la respuesta y metadata
        """

        if not self.ai_provider:
            raise AIServiceError("AI provider not initialized")

        try:
            # Obtener personalidad del contexto
            personality = user_context.get('personality', {})
            system_prompt = personality.get(
                'system_prompt',
                'Eres un asistente virtual útil y amigable.'
            )

            # Obtener historial de conversación
            conversation_history = user_context.get('history', [])

            # Generar respuesta
            logger.info(f"Generating AI response for message: {message[:50]}...")

            response_text = await self.ai_provider.generate_response(
                message=message,
                system_prompt=system_prompt,
                conversation_history=conversation_history
            )

            logger.info(f"AI response generated successfully")

            return {
                'response': response_text,
                'metadata': {
                    'provider': self.ai_provider.get_name(),
                    'feature': 'ai_responses'
                }
            }

        except AIServiceError:
            # Re-lanzar errores de AI
            raise

        except Exception as e:
            logger.error(f"Unexpected error in AI processing: {e}", exc_info=True)
            raise AIServiceError(f"Unexpected error: {e}")
