from django.contrib.auth import authenticate
from rest_framework import generics, status, viewsets, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.utils import create_jwt_pair_for_user
from users.serializers import SignUpSerializer, CustomUserSerializer, UserProfileSerializer, ChangePasswordSerializer


class SignUpAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    """View for handling user signup."""
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Handle POST request to create a new user."""
        self.create(request)
        return Response({"message": "registered successfully"}, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    """View for handling user login."""
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        """Handle POST request to login a user."""
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
        """Handle GET request to retrieve current user and auth data."""
        context = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(data=context, status=status.HTTP_200_OK)


class UserProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """ViewSet for handling user profile operations."""
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Return the current user as the object to be retrieved or updated."""
        user = self.request.user
        return user


class ChangePasswordViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """ViewSet for handling password change operations."""
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Return the current user as the object to be updated."""
        user = self.request.user
        return user


class LogoutAPIView(APIView):
    """View for handling user logout."""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """Handle POST request to logout a user by blacklisting the refresh token."""
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
