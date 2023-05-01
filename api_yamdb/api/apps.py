"""
Конфиги приложения api.

ApiConfig -- Конфиг приложения api.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Конфиг приложения api."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
