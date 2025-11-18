"""
Sistema de gestión de features activables.
Implementa Strategy Pattern para cambiar comportamiento en runtime.
"""
from typing import Dict, Type, Optional, Any
from src.features.base_feature import BaseFeature
import logging

logger = logging.getLogger(__name__)


class FeatureManager:
    """
    Gestor de features que las activa/desactiva dinámicamente.
    Cada cliente puede tener diferentes features activas según su plan.
    """

    def __init__(self):
        self._available_features: Dict[str, Type[BaseFeature]] = {}
        self._active_features: Dict[str, BaseFeature] = {}

    def register_feature(self, name: str, feature_class: Type[BaseFeature]):
        """
        Registra una feature disponible para ser activada.

        Args:
            name: Nombre identificador de la feature
            feature_class: Clase que implementa BaseFeature
        """
        if not issubclass(feature_class, BaseFeature):
            raise TypeError(f"{feature_class} must inherit from BaseFeature")

        self._available_features[name] = feature_class
        logger.info(f"Feature registered: {name}")

    def enable_feature(self, name: str, config: Dict[str, Any]) -> BaseFeature:
        """
        Activa una feature con su configuración.

        Args:
            name: Nombre de la feature a activar
            config: Configuración específica de la feature

        Returns:
            Instancia de la feature activada
        """
        if name not in self._available_features:
            raise ValueError(
                f"Feature '{name}' not registered. "
                f"Available: {list(self._available_features.keys())}"
            )

        # Si ya está activa, retornar instancia existente
        if name in self._active_features:
            logger.debug(f"Feature '{name}' already active")
            return self._active_features[name]

        # Crear nueva instancia
        feature_class = self._available_features[name]
        try:
            feature_instance = feature_class(config)
            feature_instance.initialize()

            self._active_features[name] = feature_instance
            logger.info(f"Feature enabled: {name}")

            return feature_instance

        except Exception as e:
            logger.error(f"Failed to enable feature '{name}': {e}", exc_info=True)
            raise

    def disable_feature(self, name: str):
        """
        Desactiva una feature y limpia sus recursos.

        Args:
            name: Nombre de la feature a desactivar
        """
        if name not in self._active_features:
            logger.warning(f"Feature '{name}' is not active")
            return

        try:
            feature = self._active_features[name]
            feature.cleanup()
            del self._active_features[name]

            logger.info(f"Feature disabled: {name}")

        except Exception as e:
            logger.error(f"Error disabling feature '{name}': {e}", exc_info=True)
            raise

    def get_feature(self, name: str) -> Optional[BaseFeature]:
        """
        Obtiene una feature activa.

        Args:
            name: Nombre de la feature

        Returns:
            Instancia de la feature si está activa, None si no
        """
        return self._active_features.get(name)

    def is_enabled(self, name: str) -> bool:
        """
        Verifica si una feature está activa.

        Args:
            name: Nombre de la feature

        Returns:
            True si está activa, False si no
        """
        return name in self._active_features

    def list_active_features(self) -> list[str]:
        """Retorna lista de features actualmente activas"""
        return list(self._active_features.keys())

    def list_available_features(self) -> list[str]:
        """Retorna lista de features disponibles para activar"""
        return list(self._available_features.keys())

    def cleanup_all(self):
        """Limpia todas las features activas (shutdown)"""
        for name in list(self._active_features.keys()):
            try:
                self.disable_feature(name)
            except Exception as e:
                logger.error(f"Error cleaning up feature '{name}': {e}")
