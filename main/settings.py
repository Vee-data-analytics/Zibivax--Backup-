import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep  the secret key used in production secret!
SECRET_KEY = 'j974%%m0w!!#l#^i9%q*m592t@tz(clsur%3y84%l47t@2&2(*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'import_export',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'channels_redis',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',

    'crispy_forms',
    'rest_framework',
    'tinymce',
    'imagekit',

    'users.apps.UsersConfig',
    'statboard.apps.StatdashboardConfig',
]




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
    

]

X_FRAME_OPTIONS = 'SAMEORIGIN'

IMPROT_EXPORT_USE_TRANDACTIONS = True

ROOT_URLCONF = 'main.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases



DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#if DEBUG:
'''    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
'''
'''
#else:
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'zibivaxstat',
            'USER': 'zibivaxuser',
            'PASSWORD': 'Movuyi90',
            'HOST': 'localhost',
            'PORT': '5432',
    }
}
'''




# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

ASGI_APPLICATION = 'main.routing.application'

CHANNEL_LAYERS = {
    'default':{
        'BACKENDS': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'host': [('127.0.0.1.',6379),],
        }

    }
}

STATICFILES_FINDERS = {
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
}

PLOTLY_COMPONENTS = [

    'dash_core_components',
    'dash_html_components',
    'dash_renderer',

    'dpd_components',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static_in_env/'
MEDIA_URL = '/media/'
VENV_PATH = os.path.dirname(BASE_DIR)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(VENV_PATH, 'static_root')
MEDIA_ROOT = os.path.join(VENV_PATH, 'media_root')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#Django allauth
AUTHENTICATION_BACKENDS = (
#Need to login by username in django admin, regardless of alluth
'django.contrib.auth.backends.ModelBackend',
# 'allauth' specific AUTHENTICATION methods, such as login by email
'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
LOGIN_URL = 'account_login'
ACCOUNT_LOGOUT_ON_GET= 'account/login/'
LOGIN_REDIRECT_URL = ''
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_METHOD = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_PRESEVE_USERNAME_CASING = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USERNAME_BLACKLIST  = ['ADMIN','Admin','admin','God','god','GOD']
ACCOUNT_USERNAME_MIN_LENGTH = 2
ACCOUNT_UNIQUE_EMAIL = True
SITE_ID = 1


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    CSRF_TRUSTED_ORIGINS = [
    'https://zibivax-backup-production.up.railway.app',
]
