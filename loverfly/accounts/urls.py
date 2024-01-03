from django.urls import path
from .views import sign_up, get_all_users, get_user_profile_and_couple_data, update_profile_picture, update_user_settings

urlpatterns = [
    path("sign-up/", sign_up, name="sign_up"),
    path("get-all-users/", get_all_users, name="get_all_users"),
    path(
        "get-user-profile-and-couple-data/",
        get_user_profile_and_couple_data,
        name="get_user_profile_and_couple_data",
    ),
    path("update-profile-picture", update_profile_picture, name="update_profile_picture"),
    path("update-user-settings", update_user_settings, name="update_user_settings")
]
