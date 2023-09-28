from django.urls import path
from couples.views import break_up, cancel_break_up, generate_code_for_partner, get_couple, input_code_and_link_accounts

urlpatterns = [
    path(
        "get-couple/<int:couple_id>/", 
        get_couple, 
        name="get_couple"),
    path(
        "generate-code/",
        generate_code_for_partner,
        name="generatecode",
    ),
    path(
        "input-code/<str:code>/",
        input_code_and_link_accounts,
        name="inputcode",
    ),
    path(
        "breakup/",
        break_up,
        name="breakup",
    ),
    path(
        "cancel-breakup/",
        cancel_break_up,
        name="cancelbreakup"
    )
]
