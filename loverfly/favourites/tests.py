from django.test import TestCase
from django.urls import reverse

from api.tests import APISetupTests
from couples.models import Couple
from favourites.models import Fan
from accounts.models import UserProfile

# Create your tests here.

class FavouritesTests(APISetupTests, TestCase):

    def test_favourite_couple(self):
        pass

    def test_get_favourited_couples(self):
        
        # get my user profile:
        user_dict = self.main_user.data
        user_profile = UserProfile.objects.get(id=user_dict["id"])

        # favourite all couples:
        couples = Couple.objects.all()
        for couple in couples:
            Fan.objects.create(
                couple=couple,
                fan=user_profile
            )
        
        # get the favourited couples and very a successful response:
        url = reverse("get_favourited_couples")
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        self.assertEqual(response.data['api_response'], 'Success')
        self.assertEqual(response.data['number_of_favourited_couples'], 12)
        self.assertEqual(response.data['favourited_couples'][0]["partner_one"]["username"], 'Moe')
