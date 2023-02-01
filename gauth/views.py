from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import redirect
from django.conf import settings
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from django.contrib.auth import get_user_model
from users.utils import UserUtils
import requests
from django.core.files import File
import logging
from rest_framework.schemas import AutoSchema
# Create your views here.

User = get_user_model()
logger = logging.getLogger('main')

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@schema(AutoSchema)
def google_auth(request):
    google_auth_url = "https://accounts.google.com/o/oauth2/auth?scope={}&response_type=code&redirect_uri={}&client_id={}".format(
        settings.GOOGLE_OAUTH2_SCOPE,
        settings.GOOGLE_OAUTH2_REDIRECT_URI,
        settings.GOOGLE_OAUTH2_CLIENT_ID,
    )
    print(google_auth_url)
    return redirect(google_auth_url)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@schema(AutoSchema)
def google_login_callback(request):
    logger.info('ahahah')
    code = request.GET.get('code')
    if code:
        flow = InstalledAppFlow.from_client_config({"web": 
            {"auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri":"https://oauth2.googleapis.com/token",
            "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
            'project_id': "mangoread-375402",
            "client_secret": settings.GOOGLE_OAUTH2_SECRET}}, scopes=settings.GOOGLE_OAUTH2_SCOPE, redirect_uri=settings.GOOGLE_OAUTH2_REDIRECT_URI)
        flow.fetch_token(code=code)
        credentials = flow.credentials
        service = build('oauth2', 'v2', credentials=credentials)
        
        user_info = service.userinfo().get().execute()
        
        user, _ = User.objects.get_or_create(email=user_info['email'])
        user.email = user_info['email']
        user.name = user_info['name']
        
        req = requests.get(user_info['picture'])
        with open(f'/tmp/avatar.png', 'wb') as f:
            f.write(req.content)
        reopen = open(f'/tmp/avatar.png', 'rb')
        django_file = File(reopen)
        
        user.avatar.save('avatar.png', django_file, save=True)
        reopen.close()
        user.save()
        tokens = UserUtils.create_jwt_pair_for_user(user)
        return Response(data=tokens)
    else:
        return Response(data={"message": "provide code"})