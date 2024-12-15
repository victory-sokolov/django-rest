import os
import sys
from datetime import timedelta

import dynaconf
from django.contrib.messages import constants as messages
from dynaconf import Validator
from google.oauth2 import service_account

from djangoblog.logger import date_fmt

settings = dynaconf.DjangoDynaconf(
    __name__,
    environments=True,
    validators=[
        Validator(
            "DATABASES.default.PORT",
            must_exist=True,
            required=True,
            condition=lambda v: isinstance(v, int),
        ),
        Validator(
            "DATABASES.default.HOST",
            must_exist=True,
            required=True,
            condition=lambda v: isinstance(v, str),
        ),
        Validator(
            "DATABASES.default.NAME",
            must_exist=True,
            required=True,
            condition=lambda v: isinstance(v, str),
        ),
        Validator(
            "SECRET_KEY",
            must_exist=True,
            required=True,
            condition=lambda v: isinstance(v, str) and v != "",
        ),
    ],
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = None
DEBUG = True

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = "djangoblog.UserProfile"
AUTHENTICATION_BACKENDS = ("djangoblog.auth_backends.CustomUserModelBackend",)
CUSTOM_USER_MODEL = "djangoblog.models.UserProfile"
DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)

DATE_INPUT_FORMATS = "%Y-%m-%d"
DATE_FORMAT = "Y-m-d"

COLLECTFASTA_STRATEGY = "collectfasta.strategies.filesystem.FileSystemStrategy"
COLLECTFASTA_CACHE = "collectfasta"
COLLECTFASTA_DEBUG = True
COLLECTFASTA_ENABLED = True
COLLECTFASTA_THREADS = 25

# Application definition
INSTALLED_APPS = [
    "jazzmin",
    "collectfasta",
    "rest_framework",
    "django_prometheus",
    "rest_framework.authtoken",
    "extra_checks",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "drf_spectacular",
    "ckeditor",
    "corsheaders",
    "compressor",
    "ckeditor_uploader",
    "tagify",
    "dbbackup",
    "django_watchfiles",
    # app based
    "djangoblog",
    "djangoblog.api",
    "djangoblog.authentication",
]

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

CKEDITOR_UPLOAD_PATH = "uploads/"

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# Enable extra checks
# https://github.com/kalekseev/django-extra-checks
EXTRA_CHECKS = {
    "checks": [
        "field-file-upload-to",
        "field-text-null",
        "field-null",
        "field-foreign-key-db-index",
        "field-related-name",
        "no-unique-together",
        # require `db_table` for all models, increase level to CRITICAL
        {"id": "model-meta-attribute", "attrs": ["db_table"], "level": "CRITICAL"},
        # DRF
        "drf-model-serializer-extra-kwargs",
        {"id": "drf-model-serializer-meta-attribute", "attrs": ["read_only_fields"]},
    ],
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "output/static")
COMPRESS_ROOT = STATIC_ROOT
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "dmjangoblog/static"),
    os.path.join(BASE_DIR, "node_modules", "bootstrap", "dist"),
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "compressor.finders.CompressorFinder",
]

# Compressor
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
COMPRESS_CSS_HASHING_METHOD = "content"
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.rCSSMinFilter",
]
COMPRESS_JS_FILTERS = [
    "compressor.filters.jsmin.JSMinFilter",
]

CORS_ALLOW_ALL_ORIGINS = True

# Sets csrftoken cookie attributes to HttpOnly and secure
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Prevent cookies from being sent in cross-site requests
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080", "http://0.0.0.0:8080"]

# Sets X-Frame-Options header
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Permissions
STAFF_PERMISSIONS = ["view_post", "view_userprofile"]

# Database backup config
# Execute backup: ./manage.py dbbackup -z
DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": os.path.join(BASE_DIR, "backup")}
DBBACKUP_FILENAME_TEMPLATE = "{datetime}-{databasename}.{extension}"
DBBACKUP_MEDIA_FILENAME_TEMPLATE = "{datetime}-media.{extension}"


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.RemoteUserBackend",
    "django.contrib.auth.backends.ModelBackend",
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "EXCEPTION_HANDLER": "djangoblog.api.exceptions.custom_exception_handler",
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
    "SIGNING_KEY": os.getenv("SECRET_KEY"),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "BLACKLIST_AFTER_ROTATION": False,
    "JTI_CLAIM": "jti",
    "JWK_URL": None,
}

# Logging

FORMATTERS = {
    "verbose": {
        "format": "[{levelname}]: {asctime:s} {name} Thread: {threadName} {thread:d} | Module: {module} | File: {filename} {lineno:d} {name} {funcName} {process:d} {message}",
        "datefmt": date_fmt,
        "style": "{",
    },
    "simple": {
        "format": "[{levelname}]: {asctime:s} {name} | Module: {module} | File: {filename} {lineno:d} {funcName} {message}",
        "datefmt": date_fmt,
        "style": "{",
    },
    "rich": {
        "datefmt": date_fmt,
    },
}

LOGGERS = {
    "django": {
        "handlers": ["console"],
        "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        "filters": ["exclude_logs"],
        "propagate": True,
    },
    "django.request": {
        "handlers": ["logstash", "console"],
        "level": "INFO",
        "propagate": True,
    },
    "django.template": {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": True,
    },
    # Log DB queries
    "django.db.backends": {
        "level": "DEBUG",
        "handlers": ["console"],
        "propagate": True,
    },
    "gunicorn.error": {
        "handlers": [
            "console",
            "logstash",
        ],
        "level": "INFO",
    },
    "gunicorn.access": {
        "handlers": [
            "console",
            "logstash",
        ],
        "level": "INFO",
    },
}

LOGGING_HANDLERS = {
    "base": {
        "class": "logging.StreamHandler",
        "level": "INFO",
        "formatter": "simple",
    },
    "console": {
        "class": "logging.StreamHandler",
        "formatter": "verbose",
        "level": "INFO",
        "filters": ["exclude_logs"],
    },
    "rich-console": {
        "class": "rich.logging.RichHandler",
        "formatter": "rich",
        "level": "INFO",
        "filters": ["exclude_logs"],
    },
    "logstash": {
        "level": "INFO",
        "class": "logstash.TCPLogstashHandler",
        "host": "localhost",
        "port": 50000,
        "version": 1,
        "message_type": "django",
        "fqdn": False,
        "tags": ["django.request"],
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "exclude_logs": {
            "()": "djangoblog.filter.LogFilter",
        },
    },
    "formatters": FORMATTERS,
    "handlers": LOGGING_HANDLERS,
    "loggers": LOGGERS,
    "root": {
        "handlers": [],
        "level": "INFO",
        "propagate": True,
        "filters": ["exclude_logs"],
    },
}

CACHES = {
    "default": {
        "BACKEND": settings.CACHE_BACKEND,
        "LOCATION": settings.REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    },
    "tasks": {
        "BACKEND": settings.CACHE_BACKEND,
        "LOCATION": "redis://localhost",
    },
    "collectfasta": {
        "BACKEND": settings.CACHE_BACKEND,
        "LOCATION": settings.REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
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
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    # "django.middleware.cache.UpdateCacheMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "compression_middleware.middleware.CompressionMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djangoblog.middleware.RequestIdMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

# Only enable the browseable HTML API in dev (DEBUG=True)
if settings.DEBUG and "test" not in sys.argv:
    DEFAULT_RENDERER_CLASSES += ("rest_framework.renderers.BrowsableAPIRenderer",)
    INSTALLED_APPS += ["debug_toolbar", "silk"]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        "silk.middleware.SilkyMiddleware",
    ]
    SHOW_TOOLBAR_CALLBACK = True
    DEBUG_TOOLBAR_CONFIG = {"IS_RUNNING_TESTS": False}

elif "test" in sys.argv:
    NPLUSONE_RAISE = False
    INSTALLED_APPS += ["nplusone.ext.django"]
    MIDDLEWARE += ["nplusone.ext.django.NPlusOneMiddleware"]


ROOT_URLCONF = "djangoblog.urls"
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djangoblog.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DB = settings.DATABASES.default

DATABASES = {
    "default": {
        "ENGINE": DB.ENGINE,
        "NAME": DB.NAME,
        "USER": DB.USER,
        "PASSWORD": DB.PASSWORD,
        "PORT": DB.PORT,
        "HOST": DB.HOST,
        "OPTIONS": {
            "options": "-c jit=off",
            "sslmode": "require",
        },
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
USE_TZ = True

ADMIN_LANGUAGE_CODE = "en-us"

if settings.APP_ENV == "production" and settings.USE_GC_LOCAL:
    path = f"{BASE_DIR}/infra/terraform/gcp-creds.json"
    print(f"Using local GCP creds from {path}")
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(path)

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

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
        {
            "name": "Django Blog",
            "url": "home",
            "permissions": ["auth.view_user"],
        },
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


# HERE STARTS DYNACONF EXTENSION LOAD (Keep at the very bottom of settings.py)
# Read more at https://www.dynaconf.com/django/
import dynaconf  # noqa

settings = dynaconf.DjangoDynaconf(__name__)  # noqa
# HERE ENDS DYNACONF EXTENSION LOAD (No more code below this line)

if settings.APP_ENV == "production" and settings.SENTRY_ENABLED:
    import sentry_sdk
    from sentry_sdk.integrations import celery, django, redis

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[
            django.DjangoIntegration(),
            celery.CeleryIntegration(),
            redis.RedisIntegration(),
        ],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=0.2,
        send_default_pii=True,
    )
