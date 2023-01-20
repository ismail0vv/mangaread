from django.db.models import Q
from manga.models import Type, Genre, Manga, Review
from manga.serializers import MangaShortSerializer, TypeSerializer, GenreSerializer, ReviewSerializer


class MangaServices:
    @staticmethod
    def global_search_service(search_text):
        types = Type.objects.filter(Q(name__icontains=search_text))
        genres = Genre.objects.filter(Q(name__icontains=search_text))
        mangas = Manga.objects.filter(Q(title__icontains=search_text) | Q(description__icontains=search_text))
        reviews = Review.objects.filter(Q(text__icontains=search_text))

        return {"types": TypeSerializer(types, many=True).data, "genres": GenreSerializer(genres, many=True).data,
                "mangas": MangaShortSerializer(mangas, many=True).data, "reviews": ReviewSerializer(reviews, many=True).data}
