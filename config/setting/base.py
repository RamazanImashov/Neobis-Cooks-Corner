from pathlib import Path
from decouple import config
from config.setting.decompose import *
import cloudinary_storage

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = config("DEBUG", default=False)

AUTH_USER_MODEL = 'accounts.User'

INSTALLED_APPS = BASE_APPS + LIBS_APPS + APPS

# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend',
# ]

SITE_ID = 1

MIDDLEWARE = BM

ROOT_URLCONF = "config.urls"

TEMPLATES = TS

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = APVS

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

Redis_Host = config("RedisHost")

CELERY_BROKER_URL = f'redis://{Redis_Host}:6379'
CELERY_RESULT_BACKEND = f'redis://{Redis_Host}:6379'

JAZZMIN_SETTINGS = JBS
JAZZMIN_SETTINGS["show_ui_builder"] = True
JAZZMIN_UI_TWEAKS = JAZZMIN_UI_TWEAKS

REST_FRAMEWORK = RF_BS

SIMPLE_JWT = JWT_BS

SPECTACULAR_SETTINGS = SP_BS

# LOGGING = LOG_BS

CLOUDINARY_STORAGE = CLOUD_STORAGE_SETTING

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

INTERNAL_IPS = [
    "127.0.0.1",
    "192.168.31.160",
    "192.168.31.160:8000"
]


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
