from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView

from cinema_app.forms import CustomUserForm, CinemaHallForm, MovieSeanceForm, BuyingForm, ChoiceFilterForm
from cinema_app.models import CustomUser, CinemaHall, MovieSeance, Buying


class Login(LoginView):
    success_url = reverse_lazy('main_page')
    template_name = 'login.html'

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        self.request.session['last_request'] = str(timezone.now())
        return super().form_valid(form=form)


class Logout(LogoutView):
    next_page = '/'


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    success_url = '/login/'
    template_name = 'registration.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(self.object.password)
        self.object.save()
        return super().form_valid(form)


class CinemaHallCreateView(PermissionRequiredMixin, CreateView):
    model = CinemaHall
    permission_required = 'is_superuser'
    form_class = CinemaHallForm
    success_url = '/create_cinema_hall/'
    template_name = 'create_cinema_hall.html'


class MovieSeanceCreateView(PermissionRequiredMixin, CreateView):
    model = MovieSeance
    permission_required = 'is_superuser'
    form_class = MovieSeanceForm
    success_url = '/create_movie_seance/'
    template_name = 'create_movie_seance.html'

    def form_valid(self, form):
        movie = form.save(commit=False)
        hall = CinemaHall.objects.get(id=self.request.POST['show_hall'])
        movie.free_seats = hall.hall_size
        movie.save()
        return super().form_valid(form=form)


class UpdateCinemaHallView(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_superuser'
    model = CinemaHall
    form_class = CinemaHallForm
    success_url = '/'
    template_name = 'update_cinema_hall.html'


class UpdateMovieSeanceView(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_superuser'
    model = MovieSeance
    form_class = MovieSeanceForm
    success_url = '/'
    template_name = 'update_movie_seance.html'

class BuyingCreateView(LoginRequiredMixin, CreateView):
    model = Buying
    form_class = BuyingForm
    success_url = '/'
    template_name = 'buying_create.html'

    def form_valid(self, form):
        buying = form.save(commit=False)
        buying.user = self.request.user
        movie = MovieSeance.objects.get(id=self.request.POST['movie_id'])
        money = movie.price * buying.qnt
        free_seats = movie.free_seats - buying.qnt

        if free_seats < 0:
            messages.info(self.request, 'Not enough free seats!')
            return redirect('/')
        movie.free_seats -= buying.qnt
        user = self.request.user
        user.spent += money
        buying.movie_id = self.request.POST['movie_id']
        movie.save()
        user.save()
        buying.save()
        return super().form_valid(form=form)


class MovieSeanceListView(ListView):
    model = MovieSeance
    template_name = 'main.html'
    extra_context = {'buying_form': BuyingForm, }
    paginate_by = 5

    def get_queryset(self):
        dtn = timezone.now()
        td = timedelta(days=1)

        if self.request.GET.get('show_date') == 'show_today':
            return super().get_queryset().filter(show_start_date__lte=dtn, show_end_date__gt=dtn)
        elif self.request.GET.get('show_date') == 'show_tomorrow':
            return super().get_queryset().filter(show_start_date__lte=dtn + td, show_end_date__gt=dtn + td)
        return super().get_queryset().filter(show_end_date__gt=dtn)

    def get_ordering(self):
        filter_by = self.request.GET.get('filter_by')
        if filter_by == 'start':
            self.ordering = ['start_time_seance']
        elif filter_by == 'price_as':
            self.ordering = ['price']
        elif filter_by == 'price_des':
            self.ordering = ['-price']
        return self.ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort'] = ChoiceFilterForm
        return context


class BuyingListView(ListView):
    model = Buying
    template_name = 'user_buying.html'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

