"""
Django settings for the IA Tech marketing site.

Configuration is read from a `.env` file in the project root (same folder as
manage.py). The loader below is dependency-free: if `python-dotenv` is
installed it is used, otherwise a small built-in parser reads the file.
"""

from pathlib import Path
import os

# BASE_DIR = .../iatech (the folder containing manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent


def _load_env(env_path):
    """Populate os.environ from a .env file without overriding existing vars."""
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(env_path)
        return
    except Exception:
        pass

    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_env(BASE_DIR / ".env")


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default=""):
    raw = os.environ.get(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# --- Core ----------------------------------------------------------------

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-change-this-in-production-please"
)

DEBUG = env_bool("DEBUG", True)

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "127.0.0.1,localhost")

CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", "")


# --- Applications --------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "home",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "iatech.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "iatech.wsgi.application"
ASGI_APPLICATION = "iatech.asgi.application"


# --- Database ------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# --- Password validation -------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Internationalization ------------------------------------------------

LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True


# --- Static files --------------------------------------------------------

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise sirve los estáticos sin necesitar Nginx.
# USE_FINDERS=True hace que los sirva directamente desde las apps, así que
# la página funciona aunque `collectstatic` no se haya ejecutado en el deploy.
WHITENOISE_USE_FINDERS = True
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # Sin "manifest": evita el error 500 si falta el manifiesto de estáticos.
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Email (contact form) ------------------------------------------------
# El formulario envía vía la API HTTP de Resend (https://resend.com), no por
# SMTP: los hosts como Railway BLOQUEAN el puerto SMTP saliente, así que un
# envío SMTP se queda colgado y tumba el worker. HTTP (puerto 443) sí funciona.

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
# Remitente. "onboarding@resend.dev" funciona sin verificar dominio (solo puede
# enviar a tu propio correo de la cuenta Resend). Para enviar a cualquier
# dirección, verifica iatechcorp.com en Resend y usa algo como
# "IA Tech <contacto@iatechcorp.com>".
RESEND_FROM = os.environ.get("RESEND_FROM", "IA Tech <onboarding@resend.dev>")

# A dónde llegan los mensajes del formulario.
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "iatechcol1006@gmail.com")


# --- Security hardening when DEBUG is off --------------------------------

if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
