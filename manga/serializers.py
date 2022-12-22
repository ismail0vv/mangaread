from rest_framework import serializers
from .models import Type, Genre, Manga, Review
from users.serializers import CustomUserSerializer
from MangaRead.settings.settings import AUTH_USER_MODEL


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()

    class Meta:
        model = Review
        fields = 'id author text'.split()


class ReviewCreateSerializer(serializers.ModelSerializer):
    author = serializers.CurrentUserDefault()

    class Meta:
        model = Review
        fields = 'author text'.split()


class MangaSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Manga
        fields = "id title slug type genres release_year description reviews".split()
