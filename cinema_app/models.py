from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    spent = models.PositiveIntegerField(default=5000)

    def __str__(self):
        return f'Name: {self.username} ID: {self.id} spent: {self.spent}$'


class CinemaHall(models.Model):
    hall_name = models.CharField(max_length=255)
    hall_size = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Hall name: {self.hall_name}'


class MovieSeance(models.Model):
    movie_title = models.CharField(max_length=255)
    show_hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='movies')
    start_time_seance = models.TimeField(blank=True, null=True)
    end_time_seance = models.TimeField(blank=True, null=True)
    show_start_date = models.DateTimeField(blank=True, null=True)
    show_end_date = models.DateTimeField(blank=True, null=True)
    free_seats = models.PositiveSmallIntegerField(default=0)
    price = models.SmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['is_active', 'show_start_date', 'start_time_seance']

    def __str__(self):
        return f'Movie: {self.movie_title} | Price: {self.price} ' \
               f'| Start seance: {self.start_time_seance} | Start date {self.show_start_date}'


class Buying(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='purchases_user')
    movie = models.ForeignKey(MovieSeance, on_delete=models.CASCADE, related_name='purchases_movie')
    qnt = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'Movie: {self.movie} | Qnt: {self.qnt} | Spent: {self.user.spent}'
