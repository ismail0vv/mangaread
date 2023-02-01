from django.urls import path, include
from users.views import LoginAPIView, SignUpAPIView, UserProfileViewSet, ChangePasswordViewSet, LogoutAPIView, PasswordResetView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("accounts/", include("djoser.urls.jwt")),
    path("accounts/signup/", SignUpAPIView.as_view(), name='signup'),
    path("accounts/login/", LoginAPIView.as_view(), name="login"),
    path("accounts/profile/", UserProfileViewSet.as_view({'get': 'retrieve',
                                                          'put': 'update',
                                                          'patch': 'partial_update'}), name='profile'),
    path('accounts/change_password/',
         ChangePasswordViewSet.as_view({"put": "update"}), name='change-password'),
    path("accounts/logout/", LogoutAPIView.as_view(), name='logout'),
    path("reset/", PasswordResetView.as_view(), name='password-reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]
