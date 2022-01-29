from datetime import timedelta

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from cinema_app.api.filters import MyTimeRangeAndHallFilter
from cinema_app.api.serializers import CinemaHallSerializer, MovieSeanceSerializer, BuyingSerializer, \
    CustomUserSerializer
from cinema_app.models import CinemaHall, MovieSeance, Buying, CustomUser


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if created:
            token.created += timedelta(minutes=5)
            token.save()
        return Response({'token': token.key})


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        token: Token = request.auth
        token.delete()
        return Response()


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 10


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['post', ]
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny, )
        return super().get_permissions()


class CinemaHallViewSet(ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny, )
        return super().get_permissions()


class MovieSeanceViewSet(ModelViewSet):
    queryset = MovieSeance.objects.filter(show_end_date__gt=timezone.now())
    serializer_class = MovieSeanceSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['price', 'start_time_seance', ]
    filter_class = MyTimeRangeAndHallFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def get_queryset(self):
        dtn = timezone.now()
        td = timedelta(days=1)
        show_day = self.kwargs.get('show_day')
        if show_day == 'today':
            return super().get_queryset().filter(show_start_date__lte=dtn, show_end_date__gt=dtn)
        elif show_day == 'tomorrow':
            return super().get_queryset().filter(show_start_date__lte=dtn + td, show_end_date__gt=dtn + td)
        return super().get_queryset()


class BuyingViewSet(ModelViewSet):
    queryset = Buying.objects.all()
    serializer_class = BuyingSerializer
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('-id')
