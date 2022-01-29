from django_filters import rest_framework as filters
from django_filters.widgets import RangeWidget

from cinema_app.models import MovieSeance


class MyTimeRangeAndHallFilter(filters.FilterSet):
    start_time_seance = filters.TimeRangeFilter(widget=RangeWidget(attrs={'placeholder': 'hh:mm:ss'}))
    suffixes = ['min', 'max']
    show_hall = filters.CharFilter(field_name='show_hall', lookup_expr='exact')

    class Meta:
        model = MovieSeance
        fields = ('start_time_seance', 'show_hall__hall_name')
