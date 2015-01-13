#######################
# PRODUCTION SETTINGS #
#######################

import dj_database_url

from .base import *

LOGGING = {
    'version': 1,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        }
    },
}


######################
# HOST CONFIGURATION #
######################

# https://docs.djangoproject.com/en/1.7/ref/settings/#allowed-hosts
# https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['*']  #FIXME


##########################
# DATABASE CONFIGURATION #
##########################

# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# https://github.com/kennethreitz/dj-database-url
DATABASES = {
    'default': dj_database_url.config()
}


#######################
# CACHE CONFIGURATION #
#######################

# See: https://docs.djangoproject.com/en/1.7/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}


############################
# SECRET KEY CONFIGURATION #
############################

# https://docs.djangoproject.com/en/1.7/ref/settings/#secret-key
SECRET_KEY = get_env_setting('SECRET_KEY')


################################
# DJANGO STORAGE CONFIGURATION #
################################

# http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
