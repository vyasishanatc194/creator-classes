"""
Django settings for creator_class project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
from os import path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path.join(BASE_DIR, 'app'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e#krlbd^nxk$b8@6a(mosksb*)1lf@9^v^e&svv26^4c#lkab6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','3.139.122.63']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",

    'rest_framework',
    'rest_framework.authtoken',
    'social_django',
    'rest_social_auth',
    'widget_tweaks',
    'crispy_forms',

    "allauth",
    "allauth.account",
    'rest_auth.registration',
    "allauth.socialaccount",
    'allauth.socialaccount.providers.facebook',
    'rest_auth',

    'google',
    'creator',
    'user',
    'customadmin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'creator_class.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path.join(BASE_DIR, 'creator_class', 'templates'),
        ],
        'OPTIONS': {
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'creator_class.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# For server
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'creator_class',
        'USER': 'postgres',
        'HOST': 'creatorclass.cemmg26jcbac.us-east-2.rds.amazonaws.com',
        'PASSWORD': 'lOb4Rd6yq8TlYIQWAK2n',
        'PORT': '5432'
    }
}

# For local
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'creator_class',
#         'USER': 'postgres',
#         'HOST': 'localhost',
#         'PASSWORD': 'root',
#         'PORT': '5432'
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Rest Framework config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.LimitOffsetPagination'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'PAGE_SIZE' : 10,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'SEARCH_PARAM': 'q',
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # social auth
    'social_core.backends.facebook.FacebookOAuth2'
)

AUTH_USER_MODEL = 'user.User'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

MEDIA_ROOT = path.join(BASE_DIR, 'media').replace('\\', '/')

MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = "bootstrap4"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = path.join(BASE_DIR, 'static').replace('\\', '/')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    path.join(BASE_DIR, 'creator_class', 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


#Local Facebook social login
SOCIAL_AUTH_FACEBOOK_KEY = '596410561297291'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '73285fb88839658c99a3fa940fce10ca'  # App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', ]  # optional
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}  # optional


#Local Twitter social login
SOCIAL_AUTH_TWITTER_KEY = 'ekZ5wn6z1RczPQdfLDkgGDCqW'
SOCIAL_AUTH_TWITTER_SECRET = 'od6C3iKBjYlL5oaHNzp2mG6lU4dKttJ0cKlOZl9c83Mp7cxGGx'
LOGIN_REDIRECT_URL = "customadmin:user-list"

LOGIN_URL = "auth:auth_login"

LOGOUT_REDIRECT_URL = "auth:auth_login"

SITE_ID = 1

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = (
#     "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
# )


# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
# EMAIL_TIMEOUT = 5
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "webmaster.citrusbug@gmail.com"
EMAIL_HOST_PASSWORD = "mdgutpvqfeglinbh"
EMAIL_USE_TLS = True

# Stripe token
STRIPE_API_KEY = "sk_test_51I4l0BFwJZnPqrrsqMzlMuR72JD4GNsR4sf3Hd6q28xUoB2vs4hYWCf1fw1DZSYgCVsWx1w3XNhtMfZcydD0xBmv00umHC3nYO"


CURRENCY = "inr"

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5 MB