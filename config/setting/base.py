from pathlib import Path
from decouple import config
from config.setting.decompose import *
import cloudinary_storage

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = config("DEBUG", default=False)

AUTH_USER_MODEL = 'account.User'

INSTALLED_APPS = ADMIN_APPS + BASE_APPS + LIBS_APPS + APPS

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

REST_FRAMEWORK = RF_BS

SIMPLE_JWT = JWT_BS

SPECTACULAR_SETTINGS = SP_BS

LOGGING = LOG_BS

CLOUDINARY_STORAGE = CLOUD_STORAGE_SETTING

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"