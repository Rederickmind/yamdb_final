"""
Конфиги приложения reviews.

ReviewsConfig -- Конфиг приложения reviews.
"""

from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Конфиг приложения reviews."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
