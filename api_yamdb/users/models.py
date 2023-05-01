"""Импорт и переопределение модели AbstractUser."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from users.validators import validate_email_address, validate_username


class User(AbstractUser):
    """

    Переопределенный класс пользователя.

    Поля:
    username - никнейм пользователя.
    e-mail - электронная почта пользователя.
    first_name - имя пользователя.
    last_name - фамилия пользователя.
    bio - биография пользователя.
    role - роль пользователя (администратор, модератор, пользователь)

    """

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    username = models.CharField(
        max_length=150,
        verbose_name='Логин',
        help_text='Укажите логин',
        unique=True,
        null=False,
        validators=[
            validate_username
        ]
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Укажите адрес электронной почты',
        unique=True,
        null=False,
        validators=[
            validate_email_address
        ]
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Укажите Имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Укажите Фамилию',
        blank=True)
    bio = models.TextField(
        max_length=1000,
        verbose_name='Биография',
        help_text='Укажите Биографию',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLES,
        default=USER,
        max_length=15
    )

    def __str__(self):
        """Возвращает никнейм пользователя."""
        return self.username

    @property
    def is_moderator(self):
        """Присвоение пользователю роли Модератор."""
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        """Присвоение пользователю роли Администратор."""
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        """Метакласс переопределнной модели User."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
