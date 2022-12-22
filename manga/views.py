from rest_framework import generics, viewsets, permissions, mixins
from rest_framework.pagination import PageNumberPagination
from manga.filters import custom_queryset_filter
from manga.models import Type, Genre, Manga, Review
from manga.serializers import (
    TypeSerializer, GenreSerializer, MangaSerializer, ReviewSerializer, ReviewCreateSerializer
)
from users.permissions import IsAdminOrReadOnly, IsOwnerPermission


class TypeViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Type model instances."""
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Genre model instances."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)


class MangaViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Manga model instances."""
    pagination_class = PageNumberPagination
    serializer_class = MangaSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        """Returns a custom queryset based on the request parameters."""
        return custom_queryset_filter(self.request, Manga.objects.all())


class ReviewOnMangaApiView(generics.ListCreateAPIView):
    """API view for viewing and creating Review model instances for a specific Manga instance."""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Returns the Review model instances associated with the Manga instance with the provided slug."""
        slug = self.kwargs['slug']
        try:
            queryset = Review.objects.filter(manga__slug__exact=slug)
            return queryset
        except:
            raise Manga.DoesNotExist

    def get_serializer_class(self):
        """Returns the appropriate serializer class based on the request method."""
        if self.request.method in permissions.SAFE_METHODS:
            return ReviewSerializer
        return ReviewCreateSerializer

    def perform_create(self, serializer):
        """Associates the created Review model instance with the Manga instance with the provided slug."""
        serializer.validated_data['manga'] = Manga.objects.get(slug=self.kwargs['slug'])
        serializer.save()


class ReviewAPIView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """ViewSet for viewing, updating and deleting Review model instances."""
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerPermission,)
    lookup_field = 'id'
    queryset = Review.objects.all()
