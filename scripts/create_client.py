"""
Wizard interactivo para crear un nuevo cliente.
Genera archivo YAML con configuración completa.
"""
import yaml
from pathlib import Path


def create_client_wizard():
    """Wizard interactivo para crear configuración de cliente"""

    print("=" * 60)
    print("🤖 CREADOR DE CLIENTES - WhatsApp Bot Template")
    print("=" * 60)
    print()

    # Información básica
    print("📋 INFORMACIÓN BÁSICA")
    print("-" * 60)

    client_id = input("ID del cliente (slug, ej: restaurante_pepe): ").strip()
    if not client_id:
        print("❌ El ID del cliente es obligatorio")
        return

    client_name = input("Nombre del cliente: ").strip()
    if not client_name:
        print("❌ El nombre del cliente es obligatorio")
        return

    # Plan
    print()
    print("📦 PLAN DEL CLIENTE")
    print("-" * 60)
    print("1. Basic   - AI + respuestas automáticas ($200)")
    print("2. Pro     - Basic + Reservas + Analytics ($400)")
    print("3. Enterprise - Pro + Multi-Agent + CRM ($700)")

    plan_choice = input("Selecciona plan (1/2/3): ").strip()
    plan_map = {"1": "basic", "2": "pro", "3": "enterprise"}
    plan = plan_map.get(plan_choice, "basic")

    print(f"✓ Plan seleccionado: {plan}")

    # Personalidad
    print()
    print("🎭 PERSONALIDAD DEL BOT")
    print("-" * 60)

    bot_name = input(f"Nombre del bot [{client_name} Bot]: ").strip() or f"{client_name} Bot"

    print("\nTono del bot:")
    print("1. Professional - Formal y profesional")
    print("2. Friendly - Amigable y cálido")
    print("3. Casual - Informal y cercano")

    tone_choice = input("Selecciona tono (1/2/3): ").strip()
    tone_map = {"1": "professional", "2": "friendly", "3": "casual"}
    tone = tone_map.get(tone_choice, "friendly")

    print()
    description = input("Descripción del negocio (1 línea): ").strip() or f"Negocio de {client_name}"

    # Features según plan
    features = {
        "ai_responses": {
            "enabled": True,
            "config": {
                "provider": "gemini",
                "provider_config": {
                    "api_key": f"${{GEMINI_API_KEY_{client_id.upper()}}}",
                    "model": "gemini-1.5-flash",
                    "temperature": 0.8,
                    "max_tokens": 300
                }
            }
        }
    }

    # Construir config
    config = {
        "client_id": client_id,
        "client_name": client_name,
        "plan": plan,
        "features": features,
        "personality": {
            "name": bot_name,
            "tone": tone,
            "language": "es",
            "style": "conversational",
            "system_prompt": f"Eres el asistente virtual de {client_name}. {description}\nTu personalidad es {tone} y servicial.\n\nResponde de forma clara y concisa (máximo 3 oraciones).",
            "greetings": [
                f"¡Hola! Bienvenido a {client_name}",
                f"Hola, soy {bot_name}. ¿En qué puedo ayudarte?"
            ],
            "fallback_messages": [
                "No estoy seguro de cómo ayudarte con eso",
                "Déjame conectarte con alguien del equipo"
            ]
        },
        "messaging_provider": "twilio",
        "messaging_config": {
            "account_sid": f"${{TWILIO_SID_{client_id.upper()}}}",
            "auth_token": f"${{TWILIO_TOKEN_{client_id.upper()}}}",
            "whatsapp_number": f"${{TWILIO_PHONE_{client_id.upper()}}}"
        },
        "ai_provider": "gemini",
        "ai_config": {
            "api_key": f"${{GEMINI_API_KEY_{client_id.upper()}}}"
        },
        "database_url": f"sqlite+aiosqlite:///./data/{client_id}/bot.db",
        "rate_limits": {
            "messages_per_minute": 10 if plan == "basic" else 20,
            "messages_per_hour": 100 if plan == "basic" else 300
        }
    }

    # Guardar config
    config_path = Path("configs/clients") / f"{client_id}.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print()
    print("=" * 60)
    print(f"✅ Cliente creado exitosamente!")
    print("=" * 60)
    print(f"📄 Archivo: {config_path}")
    print()
    print("📁 PRÓXIMOS PASOS:")
    print()
    print(f"1. Crear directorio de datos:")
    print(f"   mkdir -p data/{client_id}")
    print()
    print(f"2. Agregar variables de entorno en .env:")
    print(f"   GEMINI_API_KEY_{client_id.upper()}=tu-api-key")
    print(f"   TWILIO_SID_{client_id.upper()}=tu-sid")
    print(f"   TWILIO_TOKEN_{client_id.upper()}=tu-token")
    print(f"   TWILIO_PHONE_{client_id.upper()}=+14155238886")
    print()
    print(f"3. Actualizar DEFAULT_CLIENT_ID en .env:")
    print(f"   DEFAULT_CLIENT_ID={client_id}")
    print()
    print("4. Reiniciar servidor:")
    print("   uvicorn src.main:app --reload")
    print()
    print("=" * 60)


if __name__ == "__main__":
    try:
        create_client_wizard()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
