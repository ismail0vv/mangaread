from django.urls import path
from gauth.views import google_auth, google_login_callback

urlpatterns = [
    path('google/', google_auth, name='google-auth'),
    path('google/callback/', google_login_callback, name='google-login-callback')
]