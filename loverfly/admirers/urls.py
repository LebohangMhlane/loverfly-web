from django.urls import path
from admirers.views import (admire_a_couple, 
                              get_admired_couples, 
                              check_if_couple_is_admired,
                              get_all_admirers)

urlpatterns = [
    path(
        "admire/<int:id>/<str:admired>/",
        admire_a_couple,
        name="favourite",
    ),
    path(
        "get-admired-couples/",
        get_admired_couples,
        name="get_favourited_couples",
    ),
    path(
        "get-all-admirers/",
        get_all_admirers,
        name="get_all_admirers",
    ),
    path(
        "check-if-admired/<int:couple_id>/",
        check_if_couple_is_admired,
        name="check_if_favourited",
    ),

]
