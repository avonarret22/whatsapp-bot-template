"""
Cliente de Twilio para enviar mensajes de WhatsApp.
"""
import os
import logging
from typing import Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)


class TwilioClient:
    """
    Cliente para enviar mensajes de WhatsApp vía Twilio.

    Configuración:
    - TWILIO_ACCOUNT_SID_{CLIENT_ID}: Account SID de Twilio
    - TWILIO_AUTH_TOKEN_{CLIENT_ID}: Auth Token de Twilio
    - TWILIO_WHATSAPP_NUMBER_{CLIENT_ID}: Número de WhatsApp de Twilio (formato: +14155238886)

    Ejemplo de uso:
        client = TwilioClient(client_id="demo_client")
        await client.send_message(
            to="+5491123456789",
            message="Hola! ¿En qué puedo ayudarte?"
        )
    """

    def __init__(self, client_id: str):
        """
        Inicializa el cliente de Twilio para un cliente específico.

        Args:
            client_id: ID del cliente (ej: "demo_client", "restaurante_pepe")
        """
        self.client_id = client_id.upper()

        # Cargar credenciales desde variables de entorno
        self.account_sid = os.getenv(f"TWILIO_ACCOUNT_SID_{self.client_id}")
        self.auth_token = os.getenv(f"TWILIO_AUTH_TOKEN_{self.client_id}")
        self.whatsapp_number = os.getenv(f"TWILIO_WHATSAPP_NUMBER_{self.client_id}")

        # Validar que las credenciales existan
        if not all([self.account_sid, self.auth_token, self.whatsapp_number]):
            logger.warning(
                f"Twilio credentials not found for client '{client_id}'. "
                f"Make sure to set TWILIO_ACCOUNT_SID_{self.client_id}, "
                f"TWILIO_AUTH_TOKEN_{self.client_id}, and "
                f"TWILIO_WHATSAPP_NUMBER_{self.client_id} in .env file"
            )
            self.client: Optional[Client] = None
        else:
            # Inicializar cliente de Twilio
            try:
                self.client = Client(self.account_sid, self.auth_token)
                logger.info(f"Twilio client initialized for '{client_id}'")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
                self.client = None

    def is_configured(self) -> bool:
        """Verifica si el cliente de Twilio está correctamente configurado."""
        return self.client is not None

    async def send_message(self, to: str, message: str) -> Optional[str]:
        """
        Envía un mensaje de WhatsApp.

        Args:
            to: Número de destino (formato: +5491123456789)
            message: Texto del mensaje a enviar

        Returns:
            Message SID si el envío fue exitoso, None si falló
        """
        if not self.is_configured():
            logger.error(
                f"Cannot send message: Twilio not configured for client '{self.client_id}'"
            )
            return None

        try:
            # Asegurar que 'to' tenga el prefijo whatsapp:
            if not to.startswith('whatsapp:'):
                to = f"whatsapp:{to}"

            # Asegurar que 'from' tenga el prefijo whatsapp:
            from_number = self.whatsapp_number
            if not from_number.startswith('whatsapp:'):
                from_number = f"whatsapp:{from_number}"

            # Enviar mensaje
            logger.info(f"Sending WhatsApp message to {to}")

            message_obj = self.client.messages.create(
                body=message,
                from_=from_number,
                to=to
            )

            logger.info(
                f"✓ Message sent successfully. SID: {message_obj.sid}, "
                f"Status: {message_obj.status}"
            )

            return message_obj.sid

        except TwilioRestException as e:
            logger.error(
                f"Twilio API error sending message: {e.code} - {e.msg}",
                exc_info=True
            )
            return None

        except Exception as e:
            logger.error(f"Unexpected error sending message: {e}", exc_info=True)
            return None

    def get_message_status(self, message_sid: str) -> Optional[str]:
        """
        Obtiene el estado de un mensaje enviado.

        Args:
            message_sid: SID del mensaje de Twilio

        Returns:
            Estado del mensaje (queued, sent, delivered, failed, etc.)
        """
        if not self.is_configured():
            logger.error("Cannot check message status: Twilio not configured")
            return None

        try:
            message = self.client.messages(message_sid).fetch()
            return message.status

        except TwilioRestException as e:
            logger.error(f"Error fetching message status: {e.code} - {e.msg}")
            return None
