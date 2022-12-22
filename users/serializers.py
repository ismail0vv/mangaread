from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from users.utils import get_photo_url

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user model.
    """

    email = serializers.EmailField(
        max_length=80, validators=[validate_email], required=True
    )
    avatar = serializers.ImageField(default="avatars/default.jpg", read_only=True)
    nickname = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"},
        validators=[validate_password], required=True
    )

    class Meta:
        model = User
        fields = "id email nickname avatar password".split()

    def get_avatar(self, user):
        """
        Get the avatar URL for a user.
        """
        return get_photo_url(self, user.avatar)


class UserProfileSerializer(CustomUserSerializer):
    """
    Serializer for the user profile.
    """

    class Meta:
        model = User
        fields = "email nickname avatar".split()

    def validate(self, attrs):
        """
        Validate the serializer data.
        """
        queryset = User.objects.exclude(id=self.context["request"].user.id)
        if queryset.filter(email=attrs["email"]).exists():
            raise ValidationError({"email": "mail already in use!"})
        if queryset.filter(nickname=attrs["nickname"]).exists():
            raise ValidationError({"nickname": "nickname already taken"})
        return attrs


class ChangePasswordSerializer(CustomUserSerializer):
    """
    Serializer for changing a user's password.
    """

    old_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["old_password", "password", "password2"]
        extra_kwargs = {
            "password": {"required": True}
        }

    def validate(self, attrs):
        """
        Validate the serializer data.
        """
        if attrs["password"] != attrs["password2"]:
            raise ValidationError({"password": "Passwords don't match"})
        return attrs

    def validate_old_password(self, old_password):
        """
        Validate the old password field.
        """
        user = self.context["request"].user
        if not user.check_password(old_password):
            raise ValidationError("Old password is not correct")

    def update(self, instance, validated_data):
        """
        Update the user's password.
        """
        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class SignUpSerializer(CustomUserSerializer):
    """
    Serializer for creating a new user.
    """

    nickname = serializers.CharField(max_length=255, required=True)
    avatar = serializers.ImageField(default="avatars/default.jpg")
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["email", "nickname", "avatar", "password", "password2", ]

    def validate_email(self, email):
        """
        Validate the email field.
        """
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise ValidationError("Email already in use!")
        return email

    def save(self, **kwargs):
        """
        Save the serializer data.
        """
        user = User(
            email=self.validated_data["email"],
            nickname=self.validated_data["nickname"],
            avatar=self.validated_data["avatar"],
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise ValidationError({"password": "Passwords don't match"})
        user.set_password(password)
        user.save()
        return user