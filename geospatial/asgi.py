# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from app import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geospatial.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/heatmap/", consumers.HeatmapConsumer.as_asgi()),
        ])
    ),
})
