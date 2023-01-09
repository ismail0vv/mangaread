from MangaRead.settings.settings import *
from MangaRead.settings.simple_jwt_settings import *
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
