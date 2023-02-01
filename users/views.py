from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from rest_framework import generics, status, viewsets, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.utils import UserUtils
from users.serializers import SignUpSerializer, CustomUserSerializer, UserProfileSerializer, ChangePasswordSerializer, PasswordResetSerializer
from django.conf import settings
from rest_framework.schemas import AutoSchema


User = get_user_model()

class SignUpAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    """View for handling user signup."""
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)
    schema = AutoSchema()

    def post(self, request):
        """Handle POST request to create a new user."""
        self.create(request)
        return Response({"message": "registered successfully"}, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    """View for handling user login."""
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer
    schema = AutoSchema()

    def post(self, request, *args, **kwargs):
        """Handle POST request to login a user."""
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = UserUtils.create_jwt_pair_for_user(user)
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
    schema = AutoSchema()

    def get_object(self):
        """Return the current user as the object to be retrieved or updated."""
        user = self.request.user
        return user


class ChangePasswordViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """ViewSet for handling password change operations."""
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    schema = AutoSchema()

    def get_object(self):
        """Return the current user as the object to be updated."""
        user = self.request.user
        return user


class LogoutAPIView(APIView):
    """View for handling user logout."""
    permission_classes = (permissions.IsAuthenticated,)
    schema = AutoSchema()

    def post(self, request):
        """Handle POST request to logout a user by blacklisting the refresh token."""
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = PasswordResetSerializer
    schema = AutoSchema()
    
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            email_body = f"Please use the link below to reset your password:\n{request.build_absolute_uri('/')}api/reset/{uid}/{token}"
            send_mail('Password reset', email_body, settings.EMAIL_HOST_USER, [email])
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'email not found'}, status=status.HTTP_404_NOT_FOUND)