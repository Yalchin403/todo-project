from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import comments.routing
from django.core.asgi import get_asgi_application


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            comments.routing.websocket_urlpatterns
        )
    ),
})