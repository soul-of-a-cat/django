import os
from pathlib import Path

from django.utils.translation import gettext_lazy
import dotenv

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOW_REVERSE_ENV = os.getenv("DJANGO_ALLOW_REVERSE", "true")
ALLOW_REVERSE = ALLOW_REVERSE_ENV in (
    "",
    "true",
    "True",
    "yes",
    "YES",
    "1",
    "y",
)

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", default="not_so_secret")

DEBUG_ENV = os.getenv("DJANGO_DEBUG", "false").lower()
DEBUG = DEBUG_ENV in ("yes", "true", "y", "1", "t")

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "core.apps.CoreConfig",
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "homepage.apps.HomepageConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "django_cleanup.apps.CleanupConfig",
    "mdeditor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "lyceum.middleware.ReverseResponseMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "lyceum.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
            ],
        },
    },
]

if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
        "localhost",
    ]
    INSTALLED_APPS.insert(6, "debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

WSGI_APPLICATION = "lyceum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DB_NAME", "db.sqlite3"),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator",
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".MinimumLengthValidator",
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".CommonPasswordValidator",
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".NumericPasswordValidator",
        ),
    },
]

LANGUAGE_CODE = os.getenv("LANGUAGE", default="ru")

TIME_ZONE = "UTC"

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ("ru", gettext_lazy("Russian")),
    ("en", gettext_lazy("English")),
    ("de", gettext_lazy("German")),
    ("fr", gettext_lazy("French")),
]

LOCALE_PATHS = ("locale",)

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_dev"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"
