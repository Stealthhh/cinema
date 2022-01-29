from django.urls import path
from rest_framework.authtoken import views

from cinema_app.api.resources import CustomAuthToken, MovieSeanceViewSet, LogoutView
from cinema_app.views import Login, Logout, UserCreateView, CinemaHallCreateView, MovieSeanceCreateView, \
    UpdateCinemaHallView, UpdateMovieSeanceView, BuyingCreateView, MovieSeanceListView, BuyingListView

urlpatterns = [
    path('', MovieSeanceListView.as_view(), name='main_page'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('create_cinema_hall/', CinemaHallCreateView.as_view(), name='create_cinema_hall'),
    path('create_movie_seance/', MovieSeanceCreateView.as_view(), name='crete_movie_seance'),
    path('update_cinema_hall/<int:pk>/', UpdateCinemaHallView.as_view(), name='update_cinema'),
    path('update_movie_seance/<int:pk>/', UpdateMovieSeanceView.as_view(), name='update_movie'),
    path('buying_create/', BuyingCreateView.as_view(), name='buying_create'),
    path('purchases/', BuyingListView.as_view(), name='purchases'),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/auth', CustomAuthToken.as_view(), name='auth'),
    path('api/logout', LogoutView.as_view(), name='api_logout'),
    path('api/seances_day/<str:show_day>/', MovieSeanceViewSet.as_view({'get': 'list',
                                                                        'post': 'create',
                                                                        'put': 'update',
                                                                        'patch': 'partial_update', }), name='show_day'),
    path('api/seances_day/<str:show_day>/<int:pk>/', MovieSeanceViewSet.as_view({'get': 'list',
                                                                                 'put': 'update',
                                                                                 'patch': 'partial_update', }),
         name='show_day'),

]

