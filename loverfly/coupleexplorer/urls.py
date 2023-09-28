from django.urls import path

from coupleexplorer.views import get_all_couples, get_trending_couples

urlpatterns = [
    path("get-all-couples/", get_all_couples, name="get_all_couples"),
    path("get-trending-couples/", get_trending_couples,
         name="get_trending_couples"),
]
