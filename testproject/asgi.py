"""
ASGI config for testproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from chat.middleware import JWTwebsocketMiddleware


application = get_asgi_application()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testproject.settings')

from channels.auth import AuthMiddlewareStack
from chat.route import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http":application,
    "websocket":JWTwebsocketMiddleware(AuthMiddlewareStack(URLRouter(websocket_urlpatterns)))
})