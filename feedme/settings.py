# coding: utf-8
# ARCHIVO DE CONFIGURACION DE BASE DE DATOS Y DEPENDENCIAS
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cp&r+-u5f*(c+jz9pdew$ktak@&lrvn9u!hov=l036wx22#!r#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# DEFINICION DE DEPENDENCIAS 
THIRD_PARTY_APPS = (
    'suit',
    'bootstrapform',
    'mathfilters',
     
    # 'session_security',
    # 'ajax_select',
    # 'autocomplete_light',
    # 'datetimewidget',
    # 'rest_framework',
    # 'ckeditor',
    # 'ckeditor_uploader',
    # 'push_notifications'
)
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)


LOCAL_APPS = (
    'webapp',
    'mobileapp',
)

INSTALLED_APPS =  THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

#CONFIGURACION DE DEPENDENCIAS Y ESTATICOS
MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.csrf",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'feedme.urls'

WSGI_APPLICATION = 'feedme.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
######CONFIGURACION DE LA BASE DE DATOS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'feedme',
        'USER': 'root',
        'PASSWORD': 'bolivar',
        'HOST': '',
        'PORT': '',
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
#CONFIGURACIONES 
LANGUAGE_CODE = 'es-BO'

TIME_ZONE = 'America/La_Paz'

USE_I18N = True

USE_L10N = True

USE_TZ = False
MAIN_APP = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(MAIN_APP, ".."))

STATIC_URL = '/static/'

STATIC_ROOT = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2] + ['static'])

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(__file__),'../media')

TEMPLATE_DIRS = (
os.path.join(os.path.dirname(__file__),'../templates'),
)

# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',

#     'django.template.loaders.cached.Loader',
#     'django.template.loaders.eggs.Loader',    
# )

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


LOGIN_REDIRECT_URL = "/"

# Redirect when login is not correct.
LOGIN_URL = '/login'



#CONFIGURACION DEL DJANGO SUIT
# Django Suit configuration example
SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Feed Me',
    'HEADER_DATE_FORMAT': 'l, j F Y',
    'HEADER_TIME_FORMAT': 'H:i a',

    # forms
    'SHOW_REQUIRED_ASTERISK': True,  # Default True
    'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    'MENU_ICONS': {
       'sites': 'icon-leaf',
       'auth': 'icon-lock',
       'feedme': ' icon-shopping-cart',
    },
}