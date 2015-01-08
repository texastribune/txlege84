#################
# BASE SETTINGS #
#################

import os

from django.core.exceptions import ImproperlyConfigured

###########
# HELPERS #
###########


def get_env_setting(setting, default=None):
    """ Get the environment setting or return exception """
    try:
        return os.environ[setting]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = ('The {} env variable was not found '
                         'and no default was set!').format(setting)
            raise ImproperlyConfigured(error_msg)


######################
# PATH CONFIGURATION #
######################

# Absolute filesystem path to the Django project directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Absolute filesystem path to the top-level project folder
SITE_DIR = os.path.dirname(BASE_DIR)


#######################
# DEBUG CONFIGURATION #
#######################

# https://docs.djangoproject.com/en/1.7/ref/settings/#debug
DEBUG = False

# https://docs.djangoproject.com/en/1.7/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG


############################
# SECRET KEY CONFIGURATION #
############################

# https://docs.djangoproject.com/en/1.7/ref/settings/#secret-key
# This key should only be used for development and testing!
SECRET_KEY = 'this_is_my_development_key'


#####################
# APP CONFIGURATION #
#####################

# https://docs.djangoproject.com/en/1.7/ref/settings/#installed-apps
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps
    'bills',
    'core',
    'committees',
    'explainers',
    'legislators',
    'topics',
)


############################
# MIDDLEWARE CONFIGURATION #
############################

# https://docs.djangoproject.com/en/1.7/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


##########################
# DATABASE CONFIGURATION #
##########################

# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


#####################
# URL CONFIGURATION #
#####################

ROOT_URLCONF = 'txlege84.urls'


######################
# WSGI CONFIGURATION #
######################

WSGI_APPLICATION = 'txlege84.wsgi.application'


#########################
# GENERAL CONFIGURATION #
#########################

# See: https://docs.djangoproject.com/en/1.7/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/1.7/ref/settings/#time-zone
TIME_ZONE = 'America/Chicago'

# See: https://docs.djangoproject.com/en/1.7/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/1.7/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/1.7/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/1.7/ref/settings/#use-tz
USE_TZ = True


##########################
# TEMPLATE CONFIGURATION #
##########################

# https://docs.djangoproject.com/en/1.7/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    os.path.join(SITE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)


#############################
# STATIC FILE CONFIGURATION #
#############################

# https://docs.djangoproject.com/en/1.7/ref/settings/#static-root
STATIC_ROOT = os.path.join(SITE_DIR, 'assets')

# https://docs.djangoproject.com/en/1.7/ref/settings/#static-url
STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/1.7/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    os.path.join(SITE_DIR, 'static'),
)


############################
# MEDIA FILE CONFIGURATION #
############################

# https://docs.djangoproject.com/en/1.7/ref/settings/#media-root
MEDIA_ROOT = os.path.join(SITE_DIR, 'media')

# https://docs.djangoproject.com/en/1.7/ref/settings/#media-url
MEDIA_URL = '/media/'


############################
# WHITENOISE CONFIGURATION #
############################

# http://whitenoise.evans.io/en/latest/django.html#add-gzip-and-caching-support
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#########################
# APP SPECIFIC SETTINGS #
#########################

ZIPPED_DATA_FILE_URL = ('http://static.openstates.org/downloads'
                        '/2014-10-02-tx-json.zip')

DOWNLOAD_DIR = os.path.join(BASE_DIR, 'data')
DOWNLOAD_PATH = os.path.join(DOWNLOAD_DIR, 'data-json.zip')

BULK_BATCH_SIZE = 10000


#######################
# OAUTH CONFIGURATION #
#######################

INSTALLED_APPS += (
    'social.apps.django_app.default',
)

SOCIAL_AUTH_TEXASTRIBUNE_KEY = get_env_setting(
    'SOCIAL_AUTH_TEXASTRIBUNE_KEY', '')
SOCIAL_AUTH_TEXASTRIBUNE_SECRET = get_env_setting(
    'SOCIAL_AUTH_TEXASTRIBUNE_SECRET', '')

AUTHENTICATION_BACKENDS = (
    'txlege84.libs.trib_authn.backend.TribOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_TEXASTRIBUNE_AUTH_EXTRA_ARGUMENTS = {
    'approval_prompt': 'auto',
}

LOGIN_REDIRECT_URL = 'landing-view'
