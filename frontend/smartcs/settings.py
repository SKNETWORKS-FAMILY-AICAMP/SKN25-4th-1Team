from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


def _parse_hosts(raw_hosts: str) -> list[str]:
    hosts = [host.strip() for host in raw_hosts.split(",") if host.strip()]
    return hosts or ["127.0.0.1", "localhost"]


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "smart-cs-dev-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() == "true"
ALLOWED_HOSTS = _parse_hosts(os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost"))

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "frontend.webui",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "frontend.smartcs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.csrf",
                "django.template.context_processors.request",
            ],
        },
    }
]

WSGI_APPLICATION = "frontend.smartcs.wsgi.application"
ASGI_APPLICATION = "frontend.smartcs.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS: list[Path] = []
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SESSION_FILE_PATH = BASE_DIR / ".django_sessions"
SESSION_FILE_PATH.mkdir(exist_ok=True)
SESSION_ENGINE = "django.contrib.sessions.backends.file"
CSRF_COOKIE_HTTPONLY = False
