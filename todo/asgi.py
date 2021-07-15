import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import comments.routing
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todo.settings")
django.setup()
application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            comments.routing.websocket_urlpatterns
        )
    ),
})
