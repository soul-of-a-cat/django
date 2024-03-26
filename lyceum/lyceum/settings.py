import os
from pathlib import Path

from django.utils.translation import gettext_lazy
import dotenv

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOW_REVERSE_ENV = os.getenv("DJANGO_ALLOW_REVERSE", "false")
ALLOW_REVERSE = ALLOW_REVERSE_ENV in (
    "",
    "true",
    "True",
    "yes",
    "YES",
    "1",
    "y",
)

X_FRAME_OPTIONS = "SAMEORIGIN"

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", default="not_so_secret")

DEBUG_ENV = os.getenv("DJANGO_DEBUG", "false").lower()
DEBUG = DEBUG_ENV in ("yes", "true", "y", "1", "t")

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "mdeditor",
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "core.apps.CoreConfig",
    "download.apps.DownloadConfig",
    "feedback.apps.FeedbackConfig",
    "homepage.apps.HomepageConfig",
    "rating.apps.RatingConfig",
    "users.apps.UsersConfig",
    "django_cleanup.apps.CleanupConfig",
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
    "users.middleware.UserMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "lyceum.urls"

TEMPLATES_DIRS = BASE_DIR / "templates"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIRS],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
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
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".NumericPasswordValidator"
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
    BASE_DIR / "static_dev",
]
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

EMAIL_HOST_USER = os.getenv("DJANGO_MAIL", default="django@mail.ru")
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "send_mail"

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/auth/login/"

DEFAULT_USER_IS_ACTIVE = os.getenv(
    "DEFAULT_USER_IS_ACTIVE",
    default=True if DEBUG else False,
)

AUTH_USER_EMAIL_UNIQUE = True

AUTHENTICATION_BACKENDS = [
    "users.backends.UserModelBackend",
    "django.contrib.auth.backends.ModelBackend",
]

MAX_AUTH_ATTEMPTS = int(os.getenv("MAX_AUTH_ATTEMPTS", default=5))
