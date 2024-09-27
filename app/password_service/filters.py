import django_filters
from app.password_service.models import ServicePassword


class ServicePasswordFilter(django_filters.FilterSet):
    service_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ServicePassword
        fields = ['service_name']
