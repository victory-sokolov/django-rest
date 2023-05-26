"""
Django settings for djangoblog project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from sentry_sdk.integrations import django, celery, redis
import sentry_sdk
from datetime import timedelta
import os
import environ

from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(os.path.join(BASE_DIR + "/djangoblog", ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# False if not in os.environ because of casting above
DEBUG = env("DEBUG")
AUTH_USER_MODEL = "djangoblog.UserProfile"
AUTHENTICATION_BACKENDS = (
    'djangoblog.auth_backends.CustomUserModelBackend',
)
CUSTOM_USER_MODEL = 'djangoblog.models.UserProfile'
DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)

DATE_INPUT_FORMATS = "%Y-%m-%d"
DATE_FORMAT = "Y-m-d"
# Application definition
INSTALLED_APPS = [
    "jazzmin",
    "watchman",
    "rest_framework",
    "rest_framework.authtoken",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "drf_spectacular",
    "debug_toolbar",
    "ckeditor",
    "corsheaders",
    "compressor",
    "ckeditor_uploader",
    "tagify",
    "dbbackup",
    # app based
    "djangoblog",
    "djangoblog.api",
    "djangoblog.authentication",
    "silk"
    # "django_elasticsearch_dsl",
]

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

CKEDITOR_UPLOAD_PATH = "uploads/"

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

# Compressor
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False

CORS_ALLOW_ALL_ORIGINS = True

# Permissions
STAFF_PERMISSIONS = [
    "view_post",
    "view_userprofile"
]

# Database backup config
# Execute backup: ./manage.py dbbackup -z
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'location': os.path.join(BASE_DIR, 'backup')
}
DBBACKUP_FILENAME_TEMPLATE = '{datetime}-{databasename}.{extension}'
DBBACKUP_MEDIA_FILENAME_TEMPLATE = '{datetime}-media.{extension}'


# Only enable the browseable HTML API in dev (DEBUG=True)
if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        "rest_framework.renderers.BrowsableAPIRenderer",
    )

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.RemoteUserBackend",
    "django.contrib.auth.backends.ModelBackend",
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "ALLOWED_VERSIONS": ["v1", "v2"],
    "DEFAULT_VERSION": "v2",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60 * 24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "BLACKLIST_AFTER_ROTATION": False,
    "JTI_CLAIM": "jti",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "rich": {"datefmt": "[%X]"},
        "simple": {
            "format": '[%(asctime)s] %(levelname)s | %(funcName)s | %(name)s | %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        'logger': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/logs/test.log',
            'formatter': 'simple',
        },
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
            "level": "INFO",
        },
        "logstash": {
            "level": "INFO",
            "class": "logstash.TCPLogstashHandler",
            "host": "localhost",
            "port": 5959,
            "version": 1,
            "message_type": "django",
            "fqdn": False,
            "tags": ["django.request"],
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["logstash"],
            "level": "WARNING",
            "propagate": True,
        },
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": True,
        },
        # Log DB queries
        "django.db.backends": {
            "level": "DEBUG",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
        'propagate': False,
    },
}

# CONN_MAX_AGE = 5

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        "LOCATION": "redis:///host.docker.internal:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
    },
}
# CACHE_TTL = 60 * 15
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"

SPECTACULAR_SETTINGS = {
    "TITLE": "Blog API",
    "DESCRIPTION": "My blog API",
    "VERSION": "1.0.0",
    "SORT_OPERATIONS": True,
    "SORT_OPERATION_PARAMETERS": False,
    "ENABLE_LIST_MECHANICS_ON_NON_2XX": True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
    },
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_NO_READ_ONLY_REQUIRED": True,
    "SCHEMA_PATH_PREFIX_TRIM": True,
    "POSTPROCESSING_HOOKS": [
        "djangoblog.hooks.remove_schema_endpoints",
        "drf_spectacular.hooks.postprocess_schema_enums",
    ],
}

MIDDLEWARE = [
    # "django.middleware.cache.UpdateCacheMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "compression_middleware.middleware.CompressionMiddleware",
    "silk.middleware.SilkyMiddleware"
    # "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware"
]

ROOT_URLCONF = "djangoblog.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djangoblog.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "test": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mydb",
        'MIGRATE': False
    },
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "blog.sqlite3"),
    },
}

FIXTURE_DIRS = [
    "djangoblog/fixtures",
]

# default_database = env("DJANGO_DATABASE")
# DATABASES["default"] = DATABASES[default_database]

# Tests
# SOUTH_TESTS_MIGRATE = False

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

INTERNAL_IPS = ["127.0.0.1"]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGES = [
    ("en", ("English")),
    ("ru", ("Russian")),
    ("lv", ("Latvian")),
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_L10N = False
USE_TZ = True

ADMIN_LANGUAGE_CODE = "en-us"

# Celery Settings
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "djangoblog")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "djangoblog/static"),
    os.path.join(BASE_DIR, "node_modules", "bootstrap", "dist"),
]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


# ELK setup
ELASTICSEARCH_DSL = {
    "default": {"hosts": "localhost:9200"},
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

JAZZMIN_SETTINGS = {
    "site_title": "Django Blog",
    "site_icon": "images/favicon.png",
    # Add your own branding here
    "site_logo": None,
    "welcome_sign": "Welcome to the Django Blog",
    # Copyright on the footer
    "copyright": "Django Blog",
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Django Blog", "url": "home",
            "permissions": ["auth.view_user"]},
        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "users.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "admin.LogEntry": "fas fa-file",
    },
    # # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-arrow-circle-right",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {
    #     "auth.user": "collapsible",
    #     "auth.group": "vertical_tabs",
    # },
}

if not DEBUG:
    sentry_sdk.init(
        dsn="https://6e9f9287f768417e964af95f999d8678@o4505149785243648.ingest.sentry.io/4505149787930624",
        integrations=[
            django.DjangoIntegration(),
            celery.CeleryIntegration(),
            redis.RedisIntegration(),
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        send_default_pii=True
    )
