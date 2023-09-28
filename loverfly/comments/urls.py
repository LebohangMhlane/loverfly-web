from django.urls import path
from comments.views import (
    get_comments, like_comment, post_comment, delete_comment)

urlpatterns = [
    path("get-comments/<int:post_id>/", get_comments, name="get_comments"),
    path("post-comment/<int:post_id>/", post_comment, name="post_comment"),
    path("like-comment/", like_comment, name="like_comment"),
    path("delete-comment/<int:comment_id>/",
         delete_comment, name="delete_comment"),
]
