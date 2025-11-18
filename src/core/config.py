"""
Gestión de configuración del bot template.
Carga configuraciones por cliente desde archivos YAML.
"""
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, Any, Optional, Literal
from pathlib import Path
from functools import lru_cache
import yaml
import os


class FeatureConfig(BaseModel):
    """Configuración de una feature específica"""
    enabled: bool
    config: Dict[str, Any] = Field(default_factory=dict)


class ClientConfig(BaseModel):
    """Configuración completa de un cliente"""
    client_id: str
    client_name: str
    plan: Literal["basic", "pro", "enterprise"]

    # Features habilitadas
    features: Dict[str, FeatureConfig]

    # Configuración de personalidad
    personality: Dict[str, Any]

    # Configuración de mensajería
    messaging_provider: str = "twilio"
    messaging_config: Dict[str, Any]

    # Configuración de AI
    ai_provider: Literal["gemini", "claude", "openai"]
    ai_config: Dict[str, Any]

    # Base de datos
    database_url: Optional[str] = None

    # Rate limits
    rate_limits: Dict[str, int] = Field(default_factory=lambda: {
        "messages_per_minute": 10,
        "messages_per_hour": 100
    })

    # Horarios de atención
    business_hours: Optional[Dict[str, Any]] = None


class Settings(BaseSettings):
    """Configuración global de la aplicación"""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # App Settings
    app_name: str = "WhatsApp Bot Template"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    api_version: str = "v1"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Default Client
    default_client_id: str = "demo_client"

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/bot.db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Admin
    admin_api_key: str = "change-this-in-production"

    # CORS
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"


class ConfigManager:
    """
    Gestiona la carga y acceso a configuraciones de clientes.
    Implementa patrón Singleton para tener una única instancia.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.config_dir = Path("configs")
            self._clients: Dict[str, ClientConfig] = {}
            self._initialized = True
            self._load_clients()

    def _load_clients(self):
        """Carga todas las configuraciones de clientes desde archivos YAML"""
        client_configs = self.config_dir / "clients"

        if not client_configs.exists():
            print(f"Warning: Config directory {client_configs} does not exist")
            return

        for config_file in client_configs.glob("*.yaml"):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                    # Reemplazar variables de entorno en el config
                    data = self._replace_env_vars(data)

                    config = ClientConfig(**data)
                    self._clients[config.client_id] = config

                    print(f"✓ Loaded config for client: {config.client_id} ({config.plan})")

            except Exception as e:
                print(f"✗ Error loading config {config_file}: {e}")

    def _replace_env_vars(self, data: Any) -> Any:
        """Reemplaza ${VAR_NAME} con variables de entorno"""
        if isinstance(data, dict):
            return {k: self._replace_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._replace_env_vars(item) for item in data]
        elif isinstance(data, str):
            # Buscar patrón ${VAR_NAME}
            if data.startswith("${") and data.endswith("}"):
                var_name = data[2:-1]
                return os.getenv(var_name, data)
            return data
        else:
            return data

    def get_client_config(self, client_id: str) -> ClientConfig:
        """Obtiene la configuración de un cliente"""
        if client_id not in self._clients:
            raise ValueError(f"Client '{client_id}' not found. Available: {list(self._clients.keys())}")
        return self._clients[client_id]

    def list_clients(self) -> list[str]:
        """Lista todos los clientes configurados"""
        return list(self._clients.keys())

    def reload_client(self, client_id: str):
        """Recarga la configuración de un cliente específico (hot reload)"""
        config_file = self.config_dir / "clients" / f"{client_id}.yaml"

        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            data = self._replace_env_vars(data)
            config = ClientConfig(**data)
            self._clients[config.client_id] = config

        print(f"✓ Reloaded config for client: {client_id}")


@lru_cache
def get_settings() -> Settings:
    """Obtiene la configuración global de la app (cached)"""
    return Settings()


@lru_cache
def get_config_manager() -> ConfigManager:
    """Obtiene el ConfigManager (cached, singleton)"""
    return ConfigManager()
