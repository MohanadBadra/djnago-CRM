import django_filters
from django_filters import CharFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
  note = CharFilter(field_name='note', lookup_expr="icontains")
  class Meta:
    model = Order
    fields = '__all__'
    exclude = ['date_created']