"""
Фильтры приложения api.

TitleFilter -- Кастом фильтр для модели title.
"""

from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """Кастом фильтр для модели title."""

    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='contains'
    )
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='contains'
    )

    class Meta:
        """Метакласс фильтра TitleFilter."""

        model = Title
        fields = ['name', 'genre', 'category', 'year']
