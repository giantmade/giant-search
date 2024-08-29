"""
Django settings for Pancreatic Cancer Action.
"""
import os
is_console = bool(int(os.environ.get("CONSOLE", "0")))

SECRET_KEY = 'fake-key'
DEBUG = 1
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": is_console and "tests/test.sqlite" or ":memory:",
    }
}

CMS_TOOLBAR_ANONYMOUS_ON = False
CMS_ENABLE_UPDATE_CHECK = False
CMS_TEMPLATES = [
    ("base.html", "Default"),
    ("no_breadcrumb.html", "Default (No Breadcrumb)"),
    ("home_light.html", "Homepage, light navigation"),
    ("home_dark.html", "Homepage, dark navigation"),
]

ROOT_URLCONF = "tests.urls"

DEFAULT_AUTO_FIELD = u'django.db.models.AutoField'

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = False
SITE_ID = 1

SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = "SAMEORIGIN"

LANGUAGES = [
    ("en-gb", "English"),
]

DEFAULT_LANGUAGE = "en-gb"

INSTALLED_APPS = [
    "giant_search",
    "tests",

    "cms",
    "treebeard",
    "menus",
    "watson",
    # "filer",

    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    # "django.contrib.admin",
]

MIDDLEWARE = [
    "watson.middleware.SearchContextMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "cms.context_processors.cms_settings",
            ],
            "loaders": ["django.template.loaders.app_directories.Loader"],
            "debug": DEBUG,
        },
    }
]

CMS_TEMPLATES = [
    ("template.html", "Default"),
]
