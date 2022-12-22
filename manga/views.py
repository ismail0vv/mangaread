from rest_framework import generics, viewsets, views, permissions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from .models import Type, Genre, Manga, Review
from .filters import custom_queryset_filter
from users.permissions import IsAdminOrReadOnly, IsOwnerPermission
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    TypeSerializer, GenreSerializer, MangaSerializer, ReviewSerializer, ReviewCreateSerializer
)


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class MangaViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = MangaSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        return custom_queryset_filter(self.request, Manga.objects.all())


class ReviewOnMangaApiView(generics.ListCreateAPIView):

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            queryset = Review.objects.filter(manga__slug__exact=slug)
            return queryset
        except:
            return None

