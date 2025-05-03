import django_filters
from .models import Service


class ServiceFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Service
        fields = {
            'service_type': ['exact'],
        }
        order_by = ['price', 'name']
