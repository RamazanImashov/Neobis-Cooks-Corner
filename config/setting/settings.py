import os

from .base import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ["*"]

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config('DB_NAME'),
#         'USER': config('DB_USER'),
#         "PASSWORD": config('DB_PASS'),
#         'HOST': config('DB_HOST'),
#         'PORT': 5432,
#     }
# }

STATIC_URL = "/back-static/"
STATIC_ROOT = os.path.join(BASE_DIR, "back-static")

MEDIA_URL = '/back-media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "back-media")

CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:82", "http://127.0.0.1:80", "http://127.0.0.1"]


CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = ['GЕT', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS = ['Authorization', 'Content-Type']


