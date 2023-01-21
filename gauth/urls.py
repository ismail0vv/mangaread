from django.urls import path
from gauth.views import google_auth

urlpatterns = [
    path('google/', google_auth, name='google-auth')
]