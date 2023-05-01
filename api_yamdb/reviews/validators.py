"""
Валидаторы приложения reviews.

validate_one_to_ten -- Проверяет, входит ли переданное число
                       в промежуток [1, 10].
"""

from django.core.exceptions import ValidationError


def validate_one_to_ten(value, error_class=ValidationError):
    """Проверяет, входит ли переданное число в промежуток [1, 10]."""
    if not (1 <= value <= 10):
        raise error_class(
            'Оценка может быть только от 1 до 10 включительно'
        )
