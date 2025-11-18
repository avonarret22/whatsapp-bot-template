"""
Health check endpoints.
"""
from fastapi import APIRouter
from datetime import datetime
from src.core.config import get_settings, get_config_manager

router = APIRouter(tags=["health"])
settings = get_settings()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Verifica que la aplicación esté funcionando correctamente.
    """
    config_manager = get_config_manager()

    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.api_version,
        "environment": settings.environment,
        "timestamp": datetime.utcnow().isoformat(),
        "clients_loaded": len(config_manager.list_clients()),
        "clients": config_manager.list_clients()
    }


@router.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }
