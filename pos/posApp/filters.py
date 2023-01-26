from .models import Sales
import django_filters


class SalesFilter(django_filters.FilterSet):
    date_added = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Sales
        fields = ['date_added', 'code', 'grand_total']
