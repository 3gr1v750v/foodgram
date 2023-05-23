import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework.authtoken",
    "rest_framework",
    "django_filters",
    "djoser",
    "recipes.apps.RecipesConfig",
    "users.apps.UsersConfig",
    "api.apps.ApiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("ENGINE", default="django.db.backends.postgresql"),
        "NAME": os.getenv("DB_NAME", default="postgres"),
        "USER": os.getenv("POSTGRES_USER", default="postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="postgres"),
        "HOST": os.getenv("DB_HOST", default="localhost"),
        "PORT": os.getenv("DB_PORT", default=5432),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS":
        "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 6,
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "users.CustomUser"
PASSWORD_MIN_LENGTH = 8

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": PASSWORD_MIN_LENGTH,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = Path(BASE_DIR) / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(BASE_DIR) / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATABASE_FILE_UPLOAD_FOLDER = Path(BASE_DIR).parent / "data"

# Backend Model constant values for validation
DEFAULT_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254
CONTENT_MAX_LENGTH = 200
HEX_CODE_MAX_LENGTH = 7
INGREDIENT_MIN_AMOUNT = 1

# Regular Expressions for value validation
USERNAME_REGEX = r"^[\w.@+-]+\Z"
COLOR_REGEX = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"

# Error messages
UNIQUE_USERNAME = "Пользователь с таким именем уже существует!"
UNIQUE_VALUE = "Такое значение уже существует!"
UNIQUE_EMAIL = (
    "Пользователь с таким электронным почтовым адресом уже существует."
)
PASSWORD_REQUESTED_LENGTH = (
    f"Придумайте пароль длинной от {PASSWORD_MIN_LENGTH} "
    f"до {DEFAULT_MAX_LENGTH} символов.")
LESS_THAN_ONE = "Значение должно быть больше 0!"

DJOSER = {
    "PERMISSIONS": {
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_list': ['rest_framework.permissions.AllowAny'],
        'activation': ['api.permissions.DjoserEndpointsLockResponse'],
        'password_reset': ['api.permissions.DjoserEndpointsLockResponse'],
        'password_reset_confirm': ['api.permissions.DjoserEndpointsLockResponse'],
        'username_reset': ['api.permissions.DjoserEndpointsLockResponse'],
        'username_reset_confirm': ['api.permissions.DjoserEndpointsLockResponse'],
        'set_username': ['api.permissions.DjoserEndpointsLockResponse'],
    },
    "SERIALIZERS": {
        "current_user": "api.serializers.CustomUserSerializer",
    },
}

INCORRECT_LAYOUT = str.maketrans(
    "qwertyuiop[]asdfghjkl;'zxcvbnm,./", "йцукенгшщзхъфывапролджэячсмитьбю."
)
