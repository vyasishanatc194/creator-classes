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
SOCIAL_AUTH_FACEBOOK_KEY = '188875569725216'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '15ded118e17eb65bbd9bfae81f151563'  # App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', ]  # optional
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}  # optional


#Local Twitter social login
SOCIAL_AUTH_TWITTER_KEY = 'ekZ5wn6z1RczPQdfLDkgGDCqW'
SOCIAL_AUTH_TWITTER_SECRET = 'od6C3iKBjYlL5oaHNzp2mG6lU4dKttJ0cKlOZl9c83Mp7cxGGx'
LOGIN_REDIRECT_URL = "customadmin:user-list"

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
STRIPE_API_KEY = "sk_test_51I4l0BFwJZnPqrrsqMzlMuR72JD4GNsR4sf3Hd6q28xUoB2vs4hYWCf1fw1DZSYgCVsWx1w3XNhtMfZcydD0xBmv00umHC3nYO"


CURRENCY = "usd"

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5 MB

USER_SIGNUP_LINK = "http://ccmike.creatorclasses.co/user/signup/"
RESET_PASSWORD_LINK = "http://3.139.122.63/reset-password/"


PAYPAL_CLIENT_ID = "Aabc-D8rlBMneFlgavVKs9R1S5qDNcD0HXwuSP76BKM_8QGp6rhk6B1khGyRy8Bc0aELuhVIOYUImeR2"
PAYPAL_SECRET_KEY = "EOuRkF9j0KAB2mbbWruHgQCdQpZeu5MOQEASF4fklPBwNHOGxn6YHf9IBgyy0fWQefCAFfYFugy1KuKl"
PAYPAL_AUTH_TOKEN_URL = "https://api.sandbox.paypal.com/v1/oauth2/token"


AgoraAppID = "eac21ff98de64fe9b9821de92ee715a3"
AgoraAppCertificate = "3598fbec00de48bea9b968c12c246635"



SENDGRID_API_KEY='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'
CREATOR_SIGNUP_TEMPLATE = 'd-baa6392bb791427ca59e09c942358582'
FORGET_PASSWORD_TEMPLATE = 'd-4281f3a4802942adaff477e9964d4dbc'
USER_LIVE_STREAM_BOOKING_TEMPLATE = 'd-34ec6f9c567d48aaa4f22bc37081edf9'
CREATOR_LIVE_STREAM_BOOKING_TEMPLATE = 'd-531cd6df28b54a599c42954fc9734fb2'
CREATOR_SESSION_BOOKING = 'd-b7f31477db7244bcb5c6cf96bdfffa4a'
USER_SESSION_BOOKING = 'd-6b3d26650b2c419c88e5ffff26696bd0'
CREATOR_REGISTRATION_ACCEPTED_TEMPLATE = 'd-99ca283ce7ac431caaf55eb79fc9cb30'
CREATOR_REGISTRATION_REJECTED_TEMPLATE = 'd-c06e50b5680a4461b4483c9c3bc8151f'
USER_STREAM_REMINDER_TEMPLATE = 'd-9bb5f097c9eb47be8039fc169add8c82'
USER_SESSION_REMINDER_TEMPLATE = 'd-f8286e7dfe5d48709f43e3dda215315a'
CREATOR_PAYOUT_TEMPLATE = 'd-bc2f68e9864744118913a06e95996815'
CANCEL_SUBSCRIPTION_TEMPLATE = 'd-bbd3aa2c79ff4c1db9a8b55b23a1c860'


AWS_ACCESS_KEY_ID = 'AKIATDU745XSAAZYI3PX'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'creator-class-dev-bucket'
ENDPOINT_URL = "s3.amazonaws.com"
BUCKET_NAME = "creator-class-dev-bucket"
REGION_NAME = "us-east-2"
SIGNATURE_VERSION = 'v4'

AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False