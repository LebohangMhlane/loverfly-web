from django.test import TestCase
from django.urls import reverse

from api.tests import APISetupTests
from couples.models import Couple
from admirers.models import Admirer
from accounts.models import UserProfile

# Create your tests here.

class AdmirationTests(APISetupTests, TestCase):

    def test_admire_couple(self):
        pass


    def test_get_my_admirers(self):
        # get my user profile:
        user_dict = self.main_user.data
        user_profile = UserProfile.objects.get(id=user_dict["id"])
        
        # make all users admire my couple:
        user_profiles = UserProfile.objects.all().exclude(username=user_profile.username)
        my_couple = Couple.objects.filter(partner_one__username=user_profile.username).first()
        for user_profile in user_profiles:
            try:
                Admirer.objects.create(admirer=user_profile, couple=my_couple)
            except Exception as e:
                pass
        
        # make the request:
        url = reverse("get_all_admirers")
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        self.assertEqual(response.data["api_response"], "success")
        self.assertEqual(len(response.data["admirers"]), 14)
        self.assertTrue(len(response.data["next_page_link"]) > 0)
        # i should not be my own couple admirer:
        for admirer in response.data["admirers"]:
            self.assertFalse(
                admirer["admirer"]["user"]["username"] == user_profile.username
            )


    def test_get_admired_couples(self):
        # get my user profile:
        user_dict = self.main_user.data
        user_profile = UserProfile.objects.get(id=user_dict["id"])

        # admire all couples:
        couples = Couple.objects.all()
        for couple in couples:
            Admirer.objects.create(
                couple=couple,
                admirer=user_profile
            )
        
        # get the admired couples and verify a successful response:
        url = reverse("get_admired_couples")
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        self.assertEqual(response.data['api_response'], 'Success')
        self.assertEqual(response.data['number_of_admired_couples'], 10)
        self.assertEqual(response.data['admired_couples'][0]["partner_one"]["username"], 'Moe')

        # test pagination page 2:
        next_page_link = response.data["next_page_link"]
        response = self.client.get(
            next_page_link,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        self.assertEqual(response.data['api_response'], 'Success')
        self.assertEqual(response.data['number_of_favourited_couples'], 10)
        self.assertEqual(response.data['favourited_couples'][0]["partner_one"]["username"], 'Felix')

        # test pagination page 3:
        next_page_link = response.data["next_page_link"]
        response = self.client.get(
            next_page_link,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        self.assertEqual(response.data['api_response'], 'Success')
        self.assertEqual(response.data['number_of_favourited_couples'], 3)
        self.assertEqual(response.data['favourited_couples'][0]["partner_one"]["username"], 'Neo')


