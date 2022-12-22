from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register('type', TypeViewSet)
router.register('genre', GenreViewSet)
router.register('manga', MangaViewSet, basename='manga')


urlpatterns = [
    path('', include(router.urls))
]