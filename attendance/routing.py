from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"wss/attendance/(?P<room_name>\w+)/", consumers.ImageConsumer.as_asgi()),
]