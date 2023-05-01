"""
Модели приложения rewiews.

User       -- Модель пользователей.
Categories -- Модель категорий произведений.
Genre      -- Модель жанров произведений.
Title      -- Модель произведений.
Review     -- Модель отзывов.
Comment    -- Модель комментариев.
"""

import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models

from .validators import validate_one_to_ten

today = datetime.datetime.now()

User = get_user_model()


class Categories(models.Model):
    """
    Модель категорий произведений.

    name -- Название категории.
    slug -- Слаг категории.

    Методы:
    __str__ -- Возвращает название категории.

    Субклассы:
    Meta -- Метакласс модели Categories.
    """

    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex='^[-a-zA-Z0-9_]+$',
            message='slug must be Alphanumeric',
            code='invalid_slug'
        )]
    )

    def __str__(self):
        """Возвращает название категории."""
        return self.name

    class Meta:
        """Метакласс модели Categories."""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """
    Модель жанров произведений.

    name -- Название жанра.
    slug -- Слаг жанра.

    Методы:
    __str__ -- Возвращает название жанра.

    Субклассы:
    Meta -- Метакласс модели Genre.
    """

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,
                            validators=[RegexValidator(
                                regex='^[-a-zA-Z0-9_]+$',
                                message='slug must be Alphanumeric',
                                code='invalid_slug'
                            )]
                            )

    def __str__(self):
        """Возвращает название жанра."""
        return self.name

    class Meta:
        """Метакласс модели Genre."""

        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """
    Модель произведений.

    name        -- Название произведения.
    description -- Описание произведения.
    year        -- Год выпуска произведения.
    genre       -- Жанр произведения.
    category    -- Категория произведения.

    Методы:
    __str__ -- Возвращает название произведения.
    """

    name = models.CharField(verbose_name='Название', max_length=256)
    year = models.IntegerField(
        validators=[
            MaxValueValidator(today.year)
        ]
    )
    genre = models.ManyToManyField(to=Genre, related_name='title')
    category = models.ForeignKey(
        to=Categories,
        on_delete=models.SET_NULL,
        related_name='title',
        blank=True,
        null=True
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=200,
        blank=True,
        null=True
    )

    def __str__(self):
        """Возвращает название произведения."""
        return self.name


class Review(models.Model):
    """
    Модель отзывов.

    title_id -- Id произведения, к которому относится отзыв.
    text     -- Текст отзыва.
    author   -- Автор отзыва.
    score    -- Оценка произведения автором отзыва.
    pub_date -- Дата публикации отзыва.

    Субклассы:
    Meta -- Метакласс модели Review.
    """

    title = models.ForeignKey(
        to=Title,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    score = models.IntegerField(validators=[validate_one_to_ten])
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Метакласс модели Review."""

        default_related_name = 'reviews'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            ),
        )


class Comment(models.Model):
    """
    Модель комментариев.

    review_id -- Id отзыва, к которому относится комментарий.
    text      -- Текст комментария.
    author    -- Автор комментария.
    pub_date  -- Дата публикации комментария.

    Субклассы:
    Meta -- Метакласс модели Comment.
    """

    review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Метакласс модели Comment."""

        default_related_name = 'comments'
