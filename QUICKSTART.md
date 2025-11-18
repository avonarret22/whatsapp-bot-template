# 🚀 Quick Start - WhatsApp Bot Template

Guía rápida para poner en marcha el bot template.

## ⚡ Setup Rápido (5 minutos)

### 1. Instalar dependencias

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` y agregar tus credenciales:

```env
# Mínimo requerido para demo
DEFAULT_CLIENT_ID=demo_client
GEMINI_API_KEY_DEMO=tu-api-key-de-gemini
```

### 3. Ejecutar servidor

```bash
uvicorn src.main:app --reload
```

El servidor estará corriendo en: **http://localhost:8000**

### 4. Verificar que funciona

```bash
# Health check
curl http://localhost:8000/health

# Deberías ver algo como:
{
  "status": "healthy",
  "app": "WhatsApp Bot Template",
  "clients_loaded": 2,
  "clients": ["demo_client", "restaurante_pepe"]
}
```

### 5. Probar el bot (simulación)

```bash
# Simular mensaje de WhatsApp
curl -X POST "http://localhost:8000/webhook/whatsapp" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "MessageSid=SM123&From=whatsapp:+5491112345678&To=whatsapp:+14155238886&Body=Hola&NumMedia=0"

# Deberías ver en los logs la respuesta generada por el bot
```

---

## 📋 Crear un Nuevo Cliente

### Opción 1: Wizard Interactivo

```bash
python scripts/create_client.py
```

Sigue las instrucciones en pantalla.

### Opción 2: Manual

1. Copiar `configs/clients/demo_client.yaml`
2. Modificar con la info del nuevo cliente
3. Agregar variables de entorno en `.env`
4. Reiniciar servidor

---

## 🔑 Obtener API Keys

### Google Gemini (Gratis)

1. Ir a https://makersuite.google.com/app/apikey
2. Crear proyecto
3. Generar API key
4. Copiar en `.env` como `GEMINI_API_KEY_DEMO`

### Twilio WhatsApp (Prueba gratis)

1. Crear cuenta en https://www.twilio.com/try-twilio
2. Ir a Console → WhatsApp → Sandbox
3. Copiar credenciales:
   - Account SID → `TWILIO_SID_DEMO`
   - Auth Token → `TWILIO_TOKEN_DEMO`
   - WhatsApp number → `TWILIO_PHONE_DEMO`

---

## 📡 Exponer Webhook (Para desarrollo)

### Con Ngrok (Recomendado)

```bash
# Instalar ngrok: https://ngrok.com/download

# Exponer puerto 8000
ngrok http 8000

# Copiar URL HTTPS que te da (ej: https://abc123.ngrok.io)
# Configurar en Twilio: https://abc123.ngrok.io/webhook/whatsapp
```

### Con Railway (Deploy rápido)

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

---

## 🧪 Testing

### Test manual con cURL

```bash
# POST simulando Twilio
curl -X POST "http://localhost:8000/webhook/whatsapp" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "MessageSid=SM123&From=whatsapp:+5491112345678&To=whatsapp:+14155238886&Body=Hola%20como%20estas&NumMedia=0"
```

### Ver logs en tiempo real

```bash
uvicorn src.main:app --reload --log-level=info
```

---

## 📊 Estructura de Configuración de Cliente

```yaml
client_id: "mi_cliente"          # ID único
client_name: "Mi Negocio"        # Nombre descriptivo
plan: "basic"                    # basic|pro|enterprise

features:
  ai_responses:                  # Feature de AI
    enabled: true
    config:
      provider: "gemini"
      provider_config:
        api_key: "${GEMINI_API_KEY_MI_CLIENTE}"
        model: "gemini-1.5-flash"
        temperature: 0.8

personality:
  name: "Mi Bot"
  tone: "friendly"               # professional|friendly|casual
  system_prompt: "..."           # Instrucciones para el bot

messaging_provider: "twilio"
messaging_config:
  account_sid: "${TWILIO_SID_MI_CLIENTE}"
  # ...

rate_limits:
  messages_per_minute: 10
  messages_per_hour: 100
```

---

## 🐛 Troubleshooting

### Error: "Client 'demo_client' not found"

- Verificar que existe `configs/clients/demo_client.yaml`
- Verificar `DEFAULT_CLIENT_ID` en `.env`

### Error: "Gemini API key not provided"

- Verificar variable de entorno en `.env`
- Formato: `GEMINI_API_KEY_DEMO=tu-key-aqui` (sin comillas)

### El bot no responde

- Verificar logs del servidor
- Verificar que la feature `ai_responses` está habilitada en el YAML
- Verificar API key de Gemini

---

## 📚 Próximos Pasos

1. ✅ Personalizar la personalidad del bot en el YAML
2. ✅ Agregar más información en `system_prompt`
3. ⬜ Conectar webhook real de Twilio
4. ⬜ Implementar envío de mensajes vía Twilio
5. ⬜ Agregar base de datos para historial
6. ⬜ Implementar más features (knowledge_base, appointments)

---

## 💡 Recursos

- Documentación Gemini: https://ai.google.dev/docs
- Documentación Twilio: https://www.twilio.com/docs/whatsapp
- FastAPI Docs: https://fastapi.tiangolo.com

---

**¿Listo para vender?** 🚀

Una vez que tengas el bot funcionando localmente, puedes:
1. Hacer deploy en Railway/Render
2. Conectar con cliente real de Twilio
3. Cobrar $200-700 por setup según plan
4. Cobrar $30-50/mes por mantenimiento

¡Éxito! 💪
