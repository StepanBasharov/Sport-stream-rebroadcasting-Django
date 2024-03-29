"""
ASGI config for sportsite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import mainsite.routing
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sportsite.settings')

django.setup()

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                mainsite.routing.websocket_urlpatterns
            )
        )
    }
)
