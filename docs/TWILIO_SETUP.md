# 📱 Configuración de Twilio para WhatsApp

Esta guía te enseña cómo configurar Twilio para enviar y recibir mensajes de WhatsApp con tu bot.

---

## 🎯 Objetivo

Conectar tu bot con WhatsApp usando Twilio para:
- ✅ Recibir mensajes de usuarios
- ✅ Enviar respuestas automáticas
- ✅ Gestionar múltiples clientes con diferentes números

---

## 📋 Prerrequisitos

- Cuenta de Twilio (gratuita o de pago)
- Número de teléfono verificado
- Bot desplegado con URL pública (Ngrok, Railway, Render, etc.)

---

## 🚀 Paso 1: Crear Cuenta en Twilio

### 1.1 Registrarse

1. Ve a https://www.twilio.com/try-twilio
2. Completa el formulario de registro
3. Verifica tu email
4. Verifica tu número de teléfono

### 1.2 Obtener Credenciales

1. Inicia sesión en https://console.twilio.com
2. En el Dashboard, encontrarás:
   - **Account SID**: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **Auth Token**: Click en "Show" para verlo

**¡Guarda estas credenciales! Las necesitarás más adelante.**

---

## 📱 Paso 2: Configurar WhatsApp Sandbox (Desarrollo)

Para desarrollo, Twilio ofrece un Sandbox de WhatsApp **GRATIS** que puedes usar para probar.

### 2.1 Activar Sandbox

1. Ve a https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. Sigue las instrucciones para activar el sandbox
3. Anota el código que te dan (ej: `join xxx-yyy`)

### 2.2 Conectar tu WhatsApp

1. Abre WhatsApp en tu teléfono
2. Agrega el número de Twilio como contacto: **+1 415 523 8886**
3. Envía el mensaje: `join xxx-yyy` (el código que te dieron)
4. Recibirás confirmación de Twilio

**Número del Sandbox:**
```
+14155238886
```

### 2.3 Configurar Webhook

1. En la consola de Twilio, ve a **Messaging > Try it out > Send a WhatsApp message**
2. En "Sandbox Configuration", busca **"When a message comes in"**
3. Ingresa tu URL del webhook:
   ```
   https://tu-dominio.com/webhook/whatsapp
   ```
4. Método: **POST**
5. Guarda cambios

---

## 💳 Paso 3: Producción (Para Clientes Reales)

Para usar WhatsApp en producción necesitas un número propio de Twilio.

### 3.1 Comprar Número de Twilio

1. Ve a https://console.twilio.com/us1/develop/phone-numbers/manage/search
2. Selecciona país y características (SMS, Voice)
3. Compra el número (aproximadamente $1-2 USD/mes)

### 3.2 Habilitar WhatsApp en tu Número

1. Ve a **Messaging > Settings > WhatsApp Sender Registration**
2. Selecciona tu número
3. Completa el formulario de registro
4. Espera aprobación de Meta (1-3 días hábiles)

**Nota:** Para producción, Meta requiere que tengas un Facebook Business Manager verificado.

---

## ⚙️ Paso 4: Configurar el Bot

### 4.1 Editar archivo `.env`

Crea un archivo `.env` en la raíz del proyecto con tus credenciales:

```env
# Cliente Demo (desarrollo)
DEFAULT_CLIENT_ID="demo_client"
GEMINI_API_KEY_DEMO_CLIENT="tu-api-key-de-gemini"
TWILIO_ACCOUNT_SID_DEMO_CLIENT="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN_DEMO_CLIENT="tu-auth-token-aqui"
TWILIO_WHATSAPP_NUMBER_DEMO_CLIENT="+14155238886"
```

**Importante:**
- Reemplaza `ACxxxx` con tu Account SID real
- Reemplaza `tu-auth-token-aqui` con tu Auth Token
- Para sandbox, usa `+14155238886`
- Para producción, usa tu número comprado (ej: `+5491123456789`)

### 4.2 Verificar Configuración

Ejecuta el servidor localmente:

```bash
uvicorn src.main:app --reload
```

Ve a http://localhost:8000/docs y verifica que el endpoint `/webhook/whatsapp` esté disponible.

---

## 🧪 Paso 5: Probar el Bot

### 5.1 Con Ngrok (Local)

Si estás desarrollando localmente, usa Ngrok para exponer tu servidor:

```bash
# Instalar ngrok
winget install ngrok

# Ejecutar ngrok
ngrok http 8000
```

Ngrok te dará una URL pública: `https://xxxxx.ngrok.io`

### 5.2 Configurar Webhook en Twilio

1. Ve a la consola de Twilio
2. Actualiza el webhook con tu URL de Ngrok:
   ```
   https://xxxxx.ngrok.io/webhook/whatsapp
   ```

### 5.3 Enviar Mensaje de Prueba

1. Abre WhatsApp
2. Envía un mensaje al número de Twilio: **"Hola"**
3. Deberías recibir una respuesta del bot

**Logs del servidor:**
```
📨 WhatsApp message received: SMxxxxx from whatsapp:+5491123456789
✓ Using client: Demo Client (basic)
✓ AI response generated: Hola! ¿En qué puedo ayudarte?...
📤 Response to whatsapp:+5491123456789: Hola! ¿En qué puedo ayudarte?
✓ Message sent successfully. SID: SMxxxxx
```

---

## 🔧 Troubleshooting

### Error: "Twilio not configured for client"

**Causa:** Credenciales de Twilio no encontradas en `.env`

**Solución:**
1. Verifica que `.env` existe en la raíz del proyecto
2. Verifica que las variables tienen el formato correcto:
   ```
   TWILIO_ACCOUNT_SID_DEMO_CLIENT="ACxxxxx"
   TWILIO_AUTH_TOKEN_DEMO_CLIENT="xxxxx"
   TWILIO_WHATSAPP_NUMBER_DEMO_CLIENT="+14155238886"
   ```
3. Reinicia el servidor

### Error: "Unable to create record"

**Causa:** Número de destino no está en el sandbox

**Solución:**
1. El número que envía el mensaje debe haber enviado `join xxx-yyy` primero
2. En producción, no hay esta limitación

### El bot recibe mensajes pero no responde

**Causa:** Error en la API de Gemini o Twilio

**Solución:**
1. Verifica los logs del servidor para ver errores específicos
2. Verifica que `GEMINI_API_KEY_DEMO_CLIENT` está configurada
3. Verifica que las credenciales de Twilio son correctas

### Webhook no recibe mensajes

**Causa:** URL del webhook incorrecta o inaccesible

**Solución:**
1. Verifica que la URL es pública (no `localhost`)
2. Verifica que el endpoint es `/webhook/whatsapp` (no `/api/webhook/whatsapp`)
3. Prueba la URL en Postman para verificar que responde

---

## 💰 Costos de Twilio

### Sandbox (Desarrollo)
- **Gratis** ✅
- Limitaciones:
  - Solo usuarios que enviaron `join xxx-yyy`
  - Número compartido con otros developers
  - Marca de agua "Twilio Sandbox"

### Producción
- **Número de teléfono:** $1-2 USD/mes
- **Mensajes entrantes:** $0.005 USD c/u (~$0.005 por mensaje)
- **Mensajes salientes:**
  - Conversaciones iniciadas por usuario: **GRATIS** (primeras 1,000/mes)
  - Conversaciones iniciadas por negocio: ~$0.005-0.01 USD

**Ejemplo de costos para 1 cliente:**
- 100 conversaciones/mes = ~$1-2 USD/mes
- Es **muy barato** y puedes pasarlo al cliente

---

## 📊 Monitoreo

### Ver Logs de Mensajes en Twilio

1. Ve a https://console.twilio.com/us1/monitor/logs/sms
2. Verás todos los mensajes enviados/recibidos
3. Útil para debugging

### Estadísticas de Uso

1. Ve a https://console.twilio.com/us1/monitor/usage
2. Verás consumo y costos en tiempo real

---

## 🎓 Recursos Adicionales

- **Docs de Twilio WhatsApp:** https://www.twilio.com/docs/whatsapp
- **API Reference:** https://www.twilio.com/docs/whatsapp/api
- **Sandbox Guide:** https://www.twilio.com/docs/whatsapp/sandbox
- **Pricing:** https://www.twilio.com/whatsapp/pricing

---

## ✅ Checklist de Configuración

Antes de vender un bot, verifica:

- [ ] Cuenta de Twilio creada
- [ ] Credenciales (Account SID + Auth Token) obtenidas
- [ ] Sandbox activado y probado (desarrollo)
- [ ] Número de Twilio comprado (producción)
- [ ] WhatsApp habilitado en el número (producción)
- [ ] Variables de entorno configuradas en `.env`
- [ ] Webhook configurado en Twilio console
- [ ] Mensaje de prueba enviado y respondido
- [ ] Logs del servidor funcionando correctamente

---

## 🚀 Siguiente Paso

Una vez que Twilio está configurado, estás listo para:
1. **Deploy en Railway/Render** (ver `docs/DEPLOYMENT.md`)
2. **Vender tu primer cliente** (ver `SERVICIO_BOTS_IA.md`)

---

*Última actualización: Noviembre 2025*
