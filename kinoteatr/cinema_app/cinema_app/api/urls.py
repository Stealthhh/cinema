from rest_framework import routers

from cinema_app.api.resources import CinemaHallViewSet, MovieSeanceViewSet, BuyingViewSet, \
    CustomUserViewSet

router = routers.SimpleRouter()
router.register(r'cinema_halls', CinemaHallViewSet)
router.register(r'movie_seances', MovieSeanceViewSet)
router.register(r'buying', BuyingViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'registration', CustomUserViewSet)
urlpatterns = router.urls
