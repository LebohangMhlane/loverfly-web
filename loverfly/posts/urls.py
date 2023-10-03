from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from posts.views import create_a_post, delete_post, get_couple_posts, view_single_post

urlpatterns = [
    path("create-a-post/", create_a_post, name="create_a_post"),
    path("delete-post/<int:post_id>/", delete_post, name="delete_post"),
    path("get-couple-posts/<int:couple_id>/",
         get_couple_posts, name="get_couple_posts"),
    path("view-single-post/<int:post_id>/",
         view_single_post, name="view_single_post"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)