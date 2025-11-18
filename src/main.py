"""
Aplicación FastAPI principal del WhatsApp Bot Template.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.core.config import get_settings, get_config_manager
from src.core.feature_manager import FeatureManager
from src.features.ai_responses.feature import AIResponsesFeature
from src.api.routes import health, webhook

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    # Startup
    logger.info(f"🚀 Starting {settings.app_name} - {settings.environment}")

    # Cargar configuraciones de clientes
    config_manager = get_config_manager()
    clients = config_manager.list_clients()
    logger.info(f"📋 Loaded {len(clients)} client(s): {clients}")

    # Registrar features disponibles globalmente
    # Esto se hace una sola vez, luego cada cliente activa las que necesita
    app.state.available_features = {
        'ai_responses': AIResponsesFeature,
        # Aquí se agregan más features cuando se implementen
    }
    logger.info(f"✓ Registered {len(app.state.available_features)} feature(s)")

    logger.info("✓ Application started successfully")

    yield

    # Shutdown
    logger.info("🛑 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="WhatsApp Bot Template con IA - Multi-cliente",
    version=settings.api_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router)
app.include_router(webhook.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.api_version,
        "environment": settings.environment,
        "docs": "/docs" if settings.debug else "disabled"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
