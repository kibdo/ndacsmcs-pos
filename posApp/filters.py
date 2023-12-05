from .models import Sales
import django_filters


class SalesFilter(django_filters.FilterSet):
    date_created = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Sales
        fields = ['date_created', 'is_credit']
