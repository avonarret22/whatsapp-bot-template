"""
Webhook endpoints para recibir mensajes de WhatsApp.
"""
from fastapi import APIRouter, Request, Form, BackgroundTasks, HTTPException
from typing import Annotated
import logging

from src.core.config import get_config_manager, get_settings
from src.core.client_context import ClientContext
from src.core.feature_manager import FeatureManager
from src.core.exceptions import ClientNotFoundError, AIServiceError
from src.integrations.twilio_client import TwilioClient

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["webhook"])
settings = get_settings()


@router.post("/whatsapp")
async def whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    MessageSid: Annotated[str, Form()],
    From: Annotated[str, Form()],
    To: Annotated[str, Form()],
    Body: Annotated[str, Form()],
    NumMedia: Annotated[int, Form()] = 0,
):
    """
    Webhook para recibir mensajes de WhatsApp vía Twilio.

    Flujo:
    1. Identificar qué cliente es (por ahora usamos default_client_id)
    2. Cargar configuración del cliente
    3. Inicializar features del cliente
    4. Procesar mensaje
    5. Enviar respuesta
    """

    logger.info(f"📨 WhatsApp message received: {MessageSid} from {From}")
    logger.info(f"Message body: {Body[:100]}...")

    try:
        # PASO 1: Identificar cliente
        # Por ahora usamos el default_client_id, pero en producción
        # se puede identificar por subdomain, phone number, etc.
        client_id = settings.default_client_id

        # PASO 2: Cargar configuración del cliente
        config_manager = get_config_manager()

        try:
            client_config = config_manager.get_client_config(client_id)
        except ValueError as e:
            logger.error(f"Client not found: {client_id}")
            raise ClientNotFoundError(client_id)

        logger.info(f"✓ Using client: {client_config.client_name} ({client_config.plan})")

        # PASO 3: Inicializar features del cliente
        feature_manager = FeatureManager()

        # Obtener features disponibles del app state
        available_features = request.app.state.available_features

        # Activar solo las features habilitadas para este cliente
        for feature_name, feature_config in client_config.features.items():
            if feature_config.enabled:
                if feature_name in available_features:
                    feature_class = available_features[feature_name]
                    logger.info(f"Enabling feature: {feature_name}")

                    feature_manager.register_feature(feature_name, feature_class)
                    feature_manager.enable_feature(feature_name, feature_config.config)

                    logger.info(f"✓ Feature '{feature_name}' enabled")
                else:
                    logger.warning(f"Feature '{feature_name}' not available (not implemented yet)")

        # PASO 4: Procesar mensaje con features activas
        # Construir contexto del usuario
        user_context = {
            'phone_number': From,
            'personality': client_config.personality,
            'history': [],  # TODO: Obtener historial de BD
            'client_config': client_config
        }

        response_text = None

        # Intentar procesar con AI Responses (feature principal)
        if feature_manager.is_enabled('ai_responses'):
            ai_feature = feature_manager.get_feature('ai_responses')

            try:
                result = await ai_feature.process_message(Body, user_context)

                if result:
                    response_text = result.get('response')
                    logger.info(f"✓ AI response generated: {response_text[:50]}...")

            except AIServiceError as e:
                logger.error(f"AI service error: {e.message}")
                response_text = "Lo siento, tuve un problema al procesar tu mensaje. Intenta de nuevo."

        # Si no hay respuesta, usar mensaje de fallback
        if not response_text:
            fallback_messages = client_config.personality.get('fallback_messages', [])
            response_text = fallback_messages[0] if fallback_messages else "Lo siento, no pude procesar tu mensaje."

        # PASO 5: Enviar respuesta (en background)
        logger.info(f"📤 Response to {From}: {response_text}")

        # Enviar mensaje vía Twilio en background
        background_tasks.add_task(
            send_whatsapp_message,
            client_id=client_id,
            to=From,
            message=response_text
        )

        # TODO: Guardar conversación en base de datos
        # background_tasks.add_task(save_conversation, ...)

        # Cleanup features
        feature_manager.cleanup_all()

        return {
            "status": "success",
            "message_sid": MessageSid,
            "response_preview": response_text[:50] + "..." if len(response_text) > 50 else response_text
        }

    except ClientNotFoundError as e:
        logger.error(f"Client not found: {e.message}")
        raise HTTPException(status_code=404, detail=e.message)

    except Exception as e:
        logger.error(f"Unexpected error processing webhook: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/whatsapp")
async def whatsapp_webhook_verify():
    """
    Endpoint de verificación para Twilio (GET request).
    Twilio hace un GET para verificar que el webhook existe.
    """
    return {"status": "webhook_ready"}


async def send_whatsapp_message(client_id: str, to: str, message: str):
    """
    Envía un mensaje de WhatsApp vía Twilio (ejecutado en background).

    Args:
        client_id: ID del cliente
        to: Número de destino (ej: +5491123456789)
        message: Texto del mensaje
    """
    try:
        twilio_client = TwilioClient(client_id=client_id)

        if not twilio_client.is_configured():
            logger.warning(
                f"Twilio not configured for client '{client_id}'. "
                f"Message will not be sent: {message[:50]}..."
            )
            return

        message_sid = await twilio_client.send_message(to=to, message=message)

        if message_sid:
            logger.info(f"✓ Message sent successfully. SID: {message_sid}")
        else:
            logger.error(f"Failed to send message to {to}")

    except Exception as e:
        logger.error(f"Error in background task send_whatsapp_message: {e}", exc_info=True)
