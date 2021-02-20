"""
This is the settings file used in production.
First, it imports all default settings, then overrides respective ones.
Secrets are stored in and imported from an additional file, not set under version control.
"""

import collab_coursebook.settings_secrets as secrets

# noinspection PyUnresolvedReferences
# from collab_coursebook.settings import *

from django.utils.translation import gettext_lazy as _

### SECURITY ###

DEBUG = False

ALLOWED_HOSTS = secrets.HOSTS

SECRET_KEY = secrets.SECRET_KEY

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False


### DATABASE ###


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'HOST': 'localhost',
        'NAME': secrets.DB_NAME,
        'USER': secrets.DB_USER,
        'PASSWORD': secrets.DB_PASSWORD,
    }
}







## Allow Pdf Previewer
X_FRAME_OPTIONS = 'SAMEORIGIN'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cas_ng',
    'bootstrap4',
    'fontawesome_5',
    'base',
    'frontend',
    'content',
    'export',
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'collab_coursebook.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

CAS_SERVER_URL = "https://sso.tu-darmstadt.de/"
CAS_APPLY_ATTRIBUTES_TO_USER = True
CAS_RENAME_ATTRIBUTES = {
    'surname': 'last_name',
    'givenName': 'first_name',
    'mail': 'email',
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]

# For Django to find the translation file
# https://docs.djangoproject.com/zh-hans/3.0/topics/i18n/translation/

LOCALE_PATHS = [
    '/base/locale',
    '/collab_coursebook/locale',
    '/content/locale',
    '/frontend/locale'
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Settings for Bootstrap
BOOTSTRAP4 = {
    # Use custom CSS
    "css_url": {
        "href": STATIC_URL + "css/bootstrap.css",
    },
}

# Settings for FontAwesome
FONTAWESOME_5_CSS_URL = "//cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.css"
FONTAWESOME_5_PREFIX = "fa"

FOOTER_INFO = {
    "repo_url": "https://github.com/DataManagementLab/collab-coursebook",
    "impress_text": "",
    "impress_url": ""
}

ALLOW_PUBLIC_COURSE_EDITING_BY_EVERYONE = True






