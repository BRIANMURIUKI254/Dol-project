"""
ASGI config for Days of Light (D.O.L) ministry backend.
"""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application

# Add project directory to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Get ASGI application
django_asgi_app = get_asgi_application()

# Import and apply ASGI middleware here if needed
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import path
# 
# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             # Add WebSocket URL routing here
#             # path("ws/some_path/", SomeConsumer.as_asgi()),
#         ])
#     ),
# })

application = django_asgi_app
