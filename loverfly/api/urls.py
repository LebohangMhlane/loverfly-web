from django.urls import path
from .views import create_dummy_data, create_dummy_comments

urlpatterns = [
    # activate during DEBUG=TRUE only:
    path("create-dummy-data/", create_dummy_data, name="create_dummy_data"),
    path("create-dummy-comments/", create_dummy_comments, name="create_dummy_comments"),
]
