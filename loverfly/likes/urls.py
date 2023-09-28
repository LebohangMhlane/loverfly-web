from django.urls import path
from likes.views import like_a_post

urlpatterns = [
    path(
        "like-post/<int:post_id>/<str:post_liked>/",
            like_a_post, 
            name="like_post"
    ),
]
