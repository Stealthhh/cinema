from django import forms
from django.db.models import Q

from cinema_app.models import CustomUser, CinemaHall, Buying, MovieSeance


def q_set(start_time, end_time, start_data, end_data):
    q1 = Q(start_time_seance__range=(start_time, end_time))
    q2 = Q(end_time_seance__range=(start_time, end_time))
    q3 = Q(show_start_date__range=(start_data, end_data))
    q4 = Q(show_end_date__range=(start_data, end_data))
    q5 = Q(start_time_seance__lte=start_time, end_time_seance__gte=end_time)
    q6 = Q(show_start_date__lte=start_data, show_end_date__gte=end_data)
    return q1, q2, q3, q4, q5, q6


class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'password_confirmation',)

    def clean(self):
        data = self.cleaned_data
        if data.get('password') != data.get('password_confirmation'):
            raise forms.ValidationError('Passwords do not match!')
        return data


class CinemaHallForm(forms.ModelForm):

    class Meta:
        model = CinemaHall
        fields = '__all__'

    def clean(self):
        if self.initial:
            cleans = self.initial
            hall_id = cleans['id']
            hall_size = cleans['hall_size']
            movies = CinemaHall.objects.get(id=hall_id).movies.filter(free_seats__lt=hall_size)
            if movies:
                self.add_error('__all__', 'There are purchased tickets in this hall, cannot be changed!')
            else:
                hall_size = self.cleaned_data['hall_size']
                CinemaHall.objects.get(id=hall_id).movies.all().update(free_seats=hall_size)


class MovieSeanceForm(forms.ModelForm):

    class Meta:
        model = MovieSeance
        fields = ('movie_title', 'show_hall', 'start_time_seance', 'end_time_seance',
                  'show_start_date', 'show_end_date', 'price')
        widgets = {
            'start_time_seance': forms.TimeInput(attrs={'type': 'start_time_seance'}),
            'end_time_seance': forms.TimeInput(attrs={'type': 'end_time_seance'}),
            'show_start_date': forms.DateInput(attrs={'type': 'show_start_date'}),
            'show_end_date': forms.DateInput(attrs={'type': 'show_end_date'}),

        }

    def clean(self):
        movie = self.instance
        if self.initial:
            purchases = Buying.objects.filter(movie=movie)
            if purchases:
                self.add_error('__all__', 'Tickets for this session have already been purchased, cannot be changed!')
        cleans = self.cleaned_data
        start_time = cleans['start_time_seance']
        end_time = cleans['end_time_seance']
        start_data = cleans['show_start_date']
        end_data = cleans['show_end_date']
        show_hall = cleans['show_hall']
        q = q_set(start_time, end_time, start_data, end_data)
        movies = CinemaHall.objects.get(id=show_hall.pk)\
                           .movies.exclude(id=movie.pk).filter(q[0] | q[1] | q[4], q[2] | q[3] | q[5])
        if start_time > end_time:
            self.add_error('start_time_seance', 'Start time cannot be later than end time')
        elif start_data > end_data:
            self.add_error('show_start_date', 'Start date cannot be later than end date')
        if movies:
            self.add_error('show_hall', 'This day and this time the hall is busy! Choose another time or date!')


class BuyingForm(forms.ModelForm):

    class Meta:
        model = Buying
        fields = ('qnt', )


class ChoiceFilterForm(forms.Form):
    sort_by_price_ascending = 'price_as'
    sort_by_price_descending = 'price_des'
    sort_by_start_seance = 'start'
    sort_movies = [
        (sort_by_start_seance, 'sort by start seance'),
        (sort_by_price_ascending, 'sort by price ascending'),
        (sort_by_price_descending, 'sort by price descending')
    ]
    filter_by = forms.ChoiceField(choices=sort_movies)
