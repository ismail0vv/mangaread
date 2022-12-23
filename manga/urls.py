from django.urls import path
from manga.views import TypeViewSet, GenreViewSet, MangaViewSet, ReviewOnMangaApiView, ReviewAPIView


urlpatterns = [
    path('type/', TypeViewSet.as_view({"get": "list"})),
    path('genre/', GenreViewSet.as_view({"get": "list"})),
    path("manga/", MangaViewSet.as_view({"get": "list"})),
    path('manga/<slug:slug>/', MangaViewSet.as_view({"get": "retrieve"})),
    path('manga/<slug:slug>/reviews/', ReviewOnMangaApiView.as_view()),
    path("reviews/<int:id>/", ReviewAPIView.as_view({'get': "retrieve",
                                                     "put": "update",
                                                     "patch": "partial_update",
                                                     "delete": "destroy"}))
]
