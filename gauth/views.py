from django.shortcuts import render
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from gauth.services import get_google_userinfo
from users.utils import UserUtils
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
User = get_user_model()

# Create your views here.

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def google_auth(request):
    
    profile = get_google_userinfo()
    
    user, _ = User.objects.get_or_create(email=profile['email'], nickname=profile['name'])
    user.email = profile['email']
    user.nickname = profile['name']
    user.save()
    
    
    tokens = UserUtils.create_jwt_pair_for_user(user)

    return Response(data=tokens)