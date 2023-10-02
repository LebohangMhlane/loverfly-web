from django.urls import path
from admirers.views import (favourite_a_couple, 
                              get_favourited_couples, 
                              check_if_couple_favourited,
                              get_all_admirers)

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
        "get-all-admirers/",
        get_all_admirers,
        name="get_all_admirers",
    ),
    path(
        "check-if-favourited/<int:couple_id>/",
        check_if_couple_favourited,
        name="check_if_favourited",
    ),

]
