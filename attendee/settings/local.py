"""
Local development settings for running without Docker (e.g., on WSL).

This settings file is designed for running the application directly on your
local machine without Docker containers.

Usage:
    export DJANGO_SETTINGS_MODULE=attendee.settings.local
    python manage.py runserver
"""

import os

from .base import *

DEBUG = True
SITE_DOMAIN = "localhost:8000"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "tendee-stripe-hooks.ngrok.io"]

# Database - connects to local PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "attendee_development"),
        "USER": os.getenv("POSTGRES_USER", "attendee_development_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "attendee_development_user"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# Redis - connects to local Redis server
# Override the base.py REDIS_URL default for local development
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/5")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Chrome sandbox setting for local development
ENABLE_CHROME_SANDBOX = os.getenv("ENABLE_CHROME_SANDBOX", "false").lower() == "true"

# Storage Configuration
# Set USE_LOCAL_STORAGE=true in .env to use local filesystem instead of S3/MinIO
USE_LOCAL_STORAGE = os.getenv("USE_LOCAL_STORAGE", "false").lower() == "true"

if USE_LOCAL_STORAGE:
    # Local filesystem storage
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = "/media/"

    # Ensure media directories exist
    os.makedirs(os.path.join(MEDIA_ROOT, "recordings"), exist_ok=True)
    os.makedirs(os.path.join(MEDIA_ROOT, "screenshots"), exist_ok=True)

    LOCAL_STORAGE_BACKEND = {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_ROOT,
            "base_url": MEDIA_URL,
        },
    }

    STORAGES = {
        "default": LOCAL_STORAGE_BACKEND,
        "recordings": LOCAL_STORAGE_BACKEND,
        "bot_debug_screenshots": LOCAL_STORAGE_BACKEND,
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

    # Flag for bot controller to use local storage
    STORAGE_PROTOCOL = "local"

elif os.getenv("AWS_ENDPOINT_URL"):
    # MinIO/S3 Storage Configuration
    # MinIO requires path-style addressing (not virtual-hosted)
    import copy
    _s3_options = {
        "endpoint_url": os.getenv("AWS_ENDPOINT_URL"),
        "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
        "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "addressing_style": "path",  # Required for MinIO
        "signature_version": "s3v4",
    }
    DEFAULT_STORAGE_BACKEND = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": _s3_options,
    }
    RECORDING_STORAGE_BACKEND = copy.deepcopy(DEFAULT_STORAGE_BACKEND)
    RECORDING_STORAGE_BACKEND["OPTIONS"]["bucket_name"] = os.getenv("AWS_RECORDING_STORAGE_BUCKET_NAME")

    STORAGES = {
        "default": DEFAULT_STORAGE_BACKEND,
        "recordings": RECORDING_STORAGE_BACKEND,
        "bot_debug_screenshots": RECORDING_STORAGE_BACKEND,
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# Log more stuff in development
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "xmlschema": {"level": "WARNING", "handlers": ["console"], "propagate": False},
        # Uncomment to log database queries
        # "django.db.backends": {
        #    "handlers": ["console"],
        #    "level": "DEBUG",
        #    "propagate": False,
        # },
    },
}
