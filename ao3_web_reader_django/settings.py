"""
Django settings for ao3_web_reader_django project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

dotenv.load_dotenv(os.path.join(PROJECT_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(25))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.getenv("DEBUG", 0))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ao3_web_reader_django.apps.users',
    'ao3_web_reader_django.apps.authenticate',
    'ao3_web_reader_django.apps.core',
    'ao3_web_reader_django.apps.works',
    'ao3_web_reader_django.apps.api',
]

if DEBUG:
    INSTALLED_APPS.append('django.contrib.admin')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ao3_web_reader_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ao3_web_reader_django.wsgi.application'

# https://docs.djangoproject.com/en/4.2/ref/middleware/#cross-origin-opener-policy
SECURE_CROSS_ORIGIN_OPENER_POLICY = None


# DB Migrations
# https://docs.djangoproject.com/en/4.2/ref/settings/#migration-modules
MIGRATION_MODULES = {
    "users": "database.migrations.users",
    "core": "database.migrations.core",
    "authenticate": "database.migrations.authenticate",
    "works": "database.migrations.works",
    "api": "database.migrations.api",
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, "database", "app.sqlite3"),
    }
}

if DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": f"redis://127.0.0.1:6000/1",
        }
    }

else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": f"redis://redis:6000/1",
        }
    }

SESSION_ENGINE = "django.contrib.sessions.backends.cache"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'ao3_web_reader_django.apps.users.validators.PasswordLengthValidator',
    },
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": os.path.join(PROJECT_DIR, "logs", "log.log"),
        },
        "celery_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "simple",
            "filename": os.path.join(PROJECT_DIR, "logs", "celery_log.log"),
        },
    },
    "loggers": {
        "main": {
            "level": "INFO",
            "handlers": ["file"],
        },
        "dev": {
            "handlers": ["console"],
            "propagate": True,
            "level": "DEBUG",
        },
        "celery_logger": {
            "handlers": ["celery_file"],
            "propagate": False,
            "level": "DEBUG",
        },
    },
}

LOGGER_NAME = "dev" if DEBUG else "main"
# CELERY_LOGGER_NAME = "dev" if DEBUG else "celery_logger"
CELERY_LOGGER_NAME = "celery_logger"


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/")
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "users.User"

LOGIN_REDIRECT_URL = "core:home"
LOGIN_URL = "authenticate:login"


if DEBUG:
    CELERY_BROKER_URL = "redis://127.0.0.1:6000/2"
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6000/2"
else:
    CELERY_BROKER_URL = "redis://redis:6000/2"
    CELERY_RESULT_BACKEND = "redis://redis:6000/2"
