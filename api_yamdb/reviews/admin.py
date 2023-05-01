"""Админки для моделей приложения reviews."""

from django.contrib import admin
from reviews.models import Categories, Genre, Title

admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Categories)
