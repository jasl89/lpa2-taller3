"""
Sistema de caché para mejorar el rendimiento.
Implementa caché para consultas frecuentes.
"""

import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Gestor de caché centralizado.
    Permite limpiar el caché cuando sea necesario.
    """

    _cache_functions = []

    @classmethod
    def register(cls, func):
        """Registra una función con caché para poder limpiarla después"""
        cls._cache_functions.append(func)
        return func

    @classmethod
    def clear_all(cls):
        """Limpia todo el caché registrado"""
        for func in cls._cache_functions:
            if hasattr(func, "cache_clear"):
                func.cache_clear()
                logger.info(f"Caché limpiado para: {func.__name__}")


def cached_query(maxsize=128):
    """
    Decorador para cachear queries a la base de datos.

    Args:
        maxsize: Número máximo de entradas en caché
    """

    def decorator(func):
        cached_func = lru_cache(maxsize=maxsize)(func)
        CacheManager.register(cached_func)
        return cached_func

    return decorator
