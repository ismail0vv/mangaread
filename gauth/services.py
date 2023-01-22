from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage
from MangaRead.settings import base

SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.profile',
          'https://www.googleapis.com/auth/userinfo.email']



def get_google_userinfo():
    creds = None
            # flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    flow = InstalledAppFlow.from_client_config({"web": 
        {"auth_uri": "https://accounts.google.com/o/oauth2/auth",
         "token_uri":"https://oauth2.googleapis.com/token",
         "client_id": base.GOOGLE_CLIENT_ID,
         "client_secret": base.GOOGLE_SECRET}}, scopes=SCOPES)
    creds = flow.run_local_server(port=0, redirect_uri_trailing_slash=False)
    print(creds)
    try:
        service = build('oauth2', 'v2', credentials=creds)
        try:
            user_info =  service.userinfo().get().execute()
        except HttpError as error:
            print(f' Ann error occured {error}')
        
        if user_info and user_info.get('id'):
            print(user_info)
            return (user_info)
        else:
            print('pizdec')
    
    except HttpError as error:
        print(f'An error occurred: {error}')
