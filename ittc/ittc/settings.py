"""
Django settings for ittc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9u$pbamv*a1s09(5grvnko2)n)isa50=uui@lm3syhp6)jyrhg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

ITTC_APPS = (
    'ittc.capabilities',
    'ittc.cache',
    'ittc.proxy',
    'ittc.source',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
) + ITTC_APPS

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ittc.urls'

WSGI_APPLICATION = 'ittc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
#STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
STATIC_ROOT = '/var/www/ittc/static/'
STATIC_URL = '/static/'
#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, "static"),
#]
#STATICFILES_FINDERS = (
#    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#)

CACHES = {
    'default': {
        'BACKEND': 'memcachepool.cache.UMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        'OPTIONS': {
            'MAX_POOL_SIZE': 40,
            'BLACKLIST_TIME': 60,
            'SOCKET_TIMEOUT': 5,
            'MAX_ITEM_SIZE': 1000*1000*1000
        }
    },
    'tiles': {
        'BACKEND': 'memcachepool.cache.UMemcacheCache',
        'LOCATION': '127.0.0.1:11212',
        'OPTIONS': {
            'MAX_POOL_SIZE': 40,
            'BLACKLIST_TIME': 60,
            'SOCKET_TIMEOUT': 5,
            'MAX_ITEM_SIZE': 1000*1000*1000
        }
    },
    'celery_results': {
        'BACKEND': 'memcachepool.cache.UMemcacheCache',
        'LOCATION': '127.0.0.1:11213',
        'OPTIONS': {
            'MAX_POOL_SIZE': 40,
            'BLACKLIST_TIME': 60,
            'SOCKET_TIMEOUT': 5,
            'MAX_ITEM_SIZE': 1000*1000*1000
        }
    }
}

CELERY_CACHE_BACKEND = 'default'

###Settings ITTC Capabilities
ITTC_SERVER = {
    'name': 'HIU Imagery Services',
    'cache': {
        'memory': {
            'enabled': True,
            'size': 1000,
            'minZoom': 0,
            'maxZoom': 16,
            'expiration': 'origin'
        }
    },
    'heuristic': {
        'down': {
            'enabled': True,
            'depth': 1,
            'minZoom': 0,
            'maxZoom': 18
        },
        'up': {
            'enabled': True
        },
        'nearby': {
            'enabled': True,
            'radius': 2
        }
    }
}

SITEURL = "http://localhost:8000/"

CORS_ORIGIN_ALLOW_ALL = True

PROXY_ALLOWED_HOSTS = ( 'tile.openstreetmap.org', 'tile.openstreetmap.fr', 'tiles.virtualearth.net', 'tiles.mapbox.com', 'hiu-maps.net' )

PROXY_URL = '/proxy/?url='

CELERY_RESULT_BACKEND = 'cache+memcached://127.0.0.1:11213/'
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

LOG_ROOT = BASE_DIR+'/logs'

LOG_FORMAT = {
    'tile_request': '{status}	{tilesource}	{z}	{x}	{y}	{ip}	{datetime}'
}

LOG_COLLECTION = 'logs'

CUSTOM_STATS = [
    {'name': 'total', 'collection': 'stats_total', 'attributes': []},
    {'name': 'by_ip', 'collection': 'stats_by_ip', 'attributes': ['ip']},
    {'name': 'by_source', 'collection': 'stats_by_source', 'attributes': ['source']},
    {'name': 'by_location', 'collection': 'stats_by_location', 'attributes': ['location']},
    {'name': 'by_zoom', 'collection': 'stats_by_zoom', 'attributes': ['z']},
    {'name': 'by_status', 'collection': 'stats_by_status', 'attributes': ['status']},
    {'name': 'by_year', 'collection': 'stats_by_year', 'attributes': ['year']},
    {'name': 'by_month', 'collection': 'stats_by_month', 'attributes': ['month']},
    {'name': 'by_date', 'collection': 'stats_by_date', 'attributes': ['date']},

    {'name': 'by_date_source', 'collection': 'stats_by_date_source', 'attributes': ['date', 'source']},
    {'name': 'by_ip_source', 'collection': 'stats_by_ip_source', 'attributes': ['ip', 'source']},
    {'name': 'by_source_status', 'collection': 'stats_by_source_status', 'attributes': ['source', 'status']},
    {'name': 'by_month_source', 'collection': 'stats_by_month_source', 'attributes': ['month', 'source']},
    {'name': 'by_zoom_status', 'collection': 'stats_by_zoom_status', 'attributes': ['z', 'status']},
]
