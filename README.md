# WhatsApp Bot Template con IA

Plantilla reutilizable para crear bots de WhatsApp con IA para múltiples clientes.

## Características

- **Modular**: Features activables por plan (Basic/Pro/Enterprise)
- **Multi-cliente**: Un codebase, múltiples clientes
- **Configurable**: YAML config por cliente
- **Production-ready**: FastAPI async, Redis, Docker
- **AI Flexible**: Gemini, Claude o OpenAI

## Stack Técnico

- FastAPI + Python 3.11+
- SQLAlchemy 2.0 (async)
- Redis
- Twilio WhatsApp API
- Google Gemini / Anthropic Claude
- PostgreSQL / SQLite

## Estructura del Proyecto

```
whatsapp-bot-template/
├── configs/
│   ├── clients/          # Configuración por cliente (YAML)
│   ├── features/         # Definición de features
│   └── personalities/    # Personalidades predefinidas
├── src/
│   ├── core/            # Feature Manager, Config
│   ├── features/        # Módulos enchufables
│   ├── infrastructure/  # Twilio, AI, DB
│   ├── api/            # FastAPI routes
│   └── domain/         # Entidades de negocio
├── scripts/            # Utilidades
└── tests/             # Tests
```

## Instalación

### 1. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### 4. Crear configuración de cliente

```bash
python scripts/create_client.py
```

### 5. Ejecutar servidor

```bash
uvicorn src.main:app --reload
```

## Crear Nuevo Cliente

### Opción 1: Wizard interactivo

```bash
python scripts/create_client.py
```

### Opción 2: Manual

1. Crear archivo `configs/clients/mi_cliente.yaml`
2. Configurar features según plan
3. Agregar variables de entorno
4. Reiniciar servidor

## Planes Disponibles

### Basic ($200 setup)
- AI Responses
- Knowledge Base
- Panel admin básico

### Pro ($400 setup)
- Todo lo de Basic +
- Sistema de reservas/citas
- Analytics dashboard
- Integraciones con DB

### Enterprise ($700 setup)
- Todo lo de Pro +
- Multi-agente
- Integraciones custom
- CRM integration

## Deployment

### Docker

```bash
docker-compose up -d
```

### Railway

```bash
railway up
```

### Render

Ver `render.yaml`

## Testing

```bash
# Todos los tests
pytest

# Con coverage
pytest --cov=src

# Solo unit tests
pytest tests/unit/
```

## Documentación API

Con el servidor corriendo, visitar:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Health Check

```bash
curl http://localhost:8000/health
```

## Estructura de Features

Cada feature es un módulo independiente en `src/features/`:

```python
class MyFeature(BaseFeature):
    def initialize(self): ...
    def cleanup(self): ...
    def get_routes(self): ...
    async def process_message(self, msg, ctx): ...
```

## Soporte

Para dudas y reportar bugs, abrir issue en GitHub.

## Licencia

MIT
