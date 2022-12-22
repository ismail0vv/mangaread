from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register('type', TypeViewSet)
router.register('genre', GenreViewSet)
router.register('manga', MangaViewSet, basename='manga')

urlpatterns = [
    path('', include(router.urls)),
    path('manga/<slug:slug>/reviews/', ReviewOnMangaApiView.as_view()),
    path("reviews/<int:id>/", ReviewAPIView.as_view({'get': "retrieve",
                                                     "put": "update",
                                                     "patch": "partial_update",
                                                     "delete": "destroy"}))
]
