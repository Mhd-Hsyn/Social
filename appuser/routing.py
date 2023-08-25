from django.urls import path, include
from .consumers import *
websocket_urlpatterns = [
    path("ws/ac/post/", MySyncConsumer.as_asgi()),
    # path("ws/ac/newsfeed/", NewsFeedConsumer.as_asgi()),

    
]