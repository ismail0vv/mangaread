from rest_framework import serializers
from .models import Type, Genre, Manga, Review
from users.serializers import CustomUserSerializer
from MangaRead.settings.settings import AUTH_USER_MODEL
from rest_framework.request import Request


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = 'id author text manga'.split()
        read_only_fields = "manga id author".split()


class ReviewCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = 'id author text manga'.split()
        read_only_fields = "id manga".split()


class MangaSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Manga
        fields = "id title slug type genres release_year description reviews".split()
