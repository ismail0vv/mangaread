from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from uuid import uuid4


# utils for users
def get_photo_url(serializer: serializers.ModelSerializer, photo):
    return serializer.context['request'].build_absolute_uri(photo.url)


def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return 'avatars/{}/{}.{}'.format(instance.email, uuid4().hex, ext)


def create_jwt_pair_for_user(user):
    refresh = RefreshToken.for_user(user)

    tokens = {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }

    return tokens
