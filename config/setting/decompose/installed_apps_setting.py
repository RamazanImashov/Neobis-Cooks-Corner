BASE_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django.contrib.sites',
    "django.contrib.flatpages",
]

LIBS_APPS = [
    "debug_toolbar",
    'drf_spectacular',
    "rest_framework",
    "corsheaders",
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    "cloudinary",
    "cloudinary_storage",
    "django_filters",
]

APPS = [
    "accounts",
    "apps.user_profile",
    "apps.recipe",
    "apps.review",
]

