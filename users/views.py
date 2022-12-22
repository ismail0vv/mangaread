from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignUpSerializer, CustomUserSerializer, UserProfileSerializer, ChangePasswordSerializer
from rest_framework import generics, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework import permissions
from .utils import create_jwt_pair_for_user
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwnerPermission
from django.shortcuts import get_object_or_404
from MangaRead.settings.settings import AUTH_USER_MODEL


class SignUpAPIView(mixins.CreateModelMixin,
                    generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        self.create(request)
        return Response({"message": "registered successfully"}, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            data = {
                "message": "Login Successfully",
                "tokens": tokens
            }
            return Response(data=data, status=status.HTTP_200_OK)

        return Response(data={"message": "Wrong email or password!"})

    def get(self, request):
        context = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(data=context, status=status.HTTP_200_OK)


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        return user


class ChangePasswordViewSet(mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        return user


class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)