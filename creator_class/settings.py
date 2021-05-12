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
import environ


env = environ.Env()
environ.Env.read_env(str(".env"))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, path.join(BASE_DIR, 'app'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e#krlbd^nxk$b8@6a(mosksb*)1lf@9^v^e&svv26^4c#lkab6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','3.139.122.63', 'admin.creatorclasses.co']


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
    'rest_auth',
    # 'agora',

    "allauth",
    "allauth.account",
    'rest_auth.registration',
    "allauth.socialaccount",
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    # 'rest_auth',
    # 'dj_rest_auth',
    
    'storages',

    'creator',
    'user',
    'customadmin',
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_URLS_REGEX = r"^/api/.*$"

CORS_ALLOWED_ORIGINS = [
    "http://3.139.122.63",
    "http://localhost:8080",
    "http://127.0.0.1:9000",
    "http://localhost:3002",
    "http://3.139.122.63:8000",
    "https://admin.creatorclasses.co",
]


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
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
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'HOST': env("DB_HOST"),
        'PASSWORD': env("DB_PASSWORD"),
        'PORT': env("DB_PORT")
    }
}

# For local
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'creator_classes',
#         'USER': 'postgres',
#         'HOST': 'localhost',
#         'PASSWORD': '1234',
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
    # 'social_core.backends.facebook.FacebookOAuth2'
    'allauth.account.auth_backends.AuthenticationBackend',
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
SOCIAL_AUTH_FACEBOOK_KEY = env.str('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env.str('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', ]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}


#Local Twitter social login
SOCIAL_AUTH_TWITTER_KEY = env.str('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = env.str('SOCIAL_AUTH_TWITTER_SECRET')
LOGIN_REDIRECT_URL = 'customadmin:user-list'

LOGIN_URL = "auth:auth_login"

LOGOUT_REDIRECT_URL = "auth:auth_login"

SITE_ID = 2

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
STRIPE_API_KEY = env.str('STRIPE_API_KEY')


CURRENCY = "gbp"

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5 MB

USER_SIGNUP_LINK = "http://ccmike.creatorclasses.co/user/signup/"
RESET_PASSWORD_LINK = "http://ccmike.creatorclasses.co/user/forgot-password/"


PAYPAL_CLIENT_ID = env.str('PAYPAL_CLIENT_ID')
PAYPAL_SECRET_KEY = env.str('PAYPAL_SECRET_KEY')
PAYPAL_AUTH_TOKEN_URL = env.str('PAYPAL_AUTH_TOKEN_URL')


AgoraAppID = env.str('AgoraAppID')
AgoraAppCertificate = env.str('AgoraAppCertificate')

SENDGRID_API_KEY = env.str('SENDGRID_API_KEY')
CREATOR_SIGNUP_TEMPLATE = env.str('CREATOR_SIGNUP_TEMPLATE')
FORGET_PASSWORD_TEMPLATE = env.str('FORGET_PASSWORD_TEMPLATE')
USER_LIVE_STREAM_BOOKING_TEMPLATE = env.str('USER_LIVE_STREAM_BOOKING_TEMPLATE')
CREATOR_LIVE_STREAM_BOOKING_TEMPLATE = env.str('CREATOR_LIVE_STREAM_BOOKING_TEMPLATE')
CREATOR_SESSION_BOOKING = env.str('CREATOR_SESSION_BOOKING')
USER_SESSION_BOOKING = env.str('USER_SESSION_BOOKING')
CREATOR_REGISTRATION_ACCEPTED_TEMPLATE = env.str('CREATOR_REGISTRATION_ACCEPTED_TEMPLATE')
CREATOR_REGISTRATION_REJECTED_TEMPLATE = env.str('CREATOR_REGISTRATION_REJECTED_TEMPLATE')
USER_STREAM_REMINDER_TEMPLATE = env.str('USER_STREAM_REMINDER_TEMPLATE')
USER_SESSION_REMINDER_TEMPLATE = env.str('USER_SESSION_REMINDER_TEMPLATE')
CREATOR_PAYOUT_TEMPLATE = env.str('CREATOR_PAYOUT_TEMPLATE')
CANCEL_SUBSCRIPTION_TEMPLATE = env.str('CANCEL_SUBSCRIPTION_TEMPLATE')

AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'myapp-user-uploads154822-dev'
ENDPOINT_URL = "s3.amazonaws.com"
BUCKET_NAME = "myapp-user-uploads154822-dev"
REGION_NAME = "us-east-2"
SIGNATURE_VERSION = 'v4'

AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False