import django_filters

from .models import Category, Genre, Title


class TitleFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = django_filters.NumberFilter(field_name='year')
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        to_field_name='slug',
    )
    genre = django_filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        field_name='genre__slug',
        to_field_name='slug',
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')
