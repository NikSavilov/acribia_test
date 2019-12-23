from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/list/(?P<key>\w+)/$', consumer.EventConsumer),
]