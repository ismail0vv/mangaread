from rest_framework import serializers
from .models import Type, Genre, Manga, Review
from users.serializers import CustomUserSerializer
from MangaRead.settings.settings import AUTH_USER_MODEL
from rest_framework.request import Request

class TypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Type model.
    """
    class Meta:
        model = Type
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Genre model.
    """
    class Meta:
        model = Genre
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    """
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = 'id author text manga'.split()
        read_only_fields = "manga id author".split()

class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new Review model instance.
    """
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = 'id author text manga'.split()
        read_only_fields = "id manga".split()

class MangaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Manga model.
    """
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Manga
        fields = "id title slug type genres release_year description reviews".split()
