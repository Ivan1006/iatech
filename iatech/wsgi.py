"""WSGI config for the iatech project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iatech.settings")

application = get_wsgi_application()
