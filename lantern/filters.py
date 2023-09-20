import django_filters

from .models import Lantern

class LanternFilter(django_filters.FilterSet):
    nickname = django_filters.CharFilter(field_name="nickname", lookup_expr='icontains')

    class Meta:
        model = Lantern
        fields = ['nickname']
