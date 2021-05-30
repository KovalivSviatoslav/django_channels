from django.urls import path

from posts.consumers import CommentsConsumer, TypingConsumer

ws_urlpatterns = [
    path('posts/<post_id>/', CommentsConsumer.as_asgi()),
    path('posts/<post_id>/typing-signal/', TypingConsumer.as_asgi())
]
