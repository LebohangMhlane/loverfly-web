from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("comments.urls")),
    path("", include("coupleexplorer.urls")),   
    path("", include("couples.urls")),
    path("", include("favourites.urls")),
    path("", include("feed.urls")),
    path("", include("likes.urls")),
    path("", include("posts.urls")),
    path("", include("accounts.urls")),
    path("api-token-auth/", views.obtain_auth_token, name="api-token-auth"),
]
