from django.urls import path

from posts.consumers import CommentsConsumer

ws_urlpatterns = [
    path('posts/<post_id>/', CommentsConsumer.as_asgi())
]
