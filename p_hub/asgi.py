"""
ASGI config for p_hub project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import participant.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'p_hub.settings')

application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        #Just HTTP for now, others protocols later

        "websocket":
                URLRouter(
                participant.routing.websocket_urlpatterns 
        )
    }
)  