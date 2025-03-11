"""
ASGI config for crpmt project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crpmt.settings')
import django
django.setup()

from django.core.asgi import get_asgi_application


application = get_asgi_application()

# Resetting the online counters on server restart
# Note: this is the least ugly option I found to update the DB at startup - it will run 4 times on each startup however
Users.objects.all().update(online=0)