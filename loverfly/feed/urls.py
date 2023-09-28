from django.urls import path
from feed.views import get_posts_for_feed

urlpatterns = [
    path("get-posts-for-feed/", get_posts_for_feed, name="get_posts_for_feed"),
]