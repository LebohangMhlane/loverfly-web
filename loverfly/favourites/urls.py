from django.urls import path
from favourites.views import (favourite_a_couple, 
                              get_favourited_couples, 
                              check_if_couple_favourited)

urlpatterns = [
    path(
        "favourite/<int:id>/<str:favourited>/",
        favourite_a_couple,
        name="favourite",
    ),
    path(
        "get-favourited-couples/",
        get_favourited_couples,
        name="get_favourited_couples",
    ),
    path(
        "check-if-favourited/<int:couple_id>/",
        check_if_couple_favourited,
        name="check_if_favourited",
    ),

]
