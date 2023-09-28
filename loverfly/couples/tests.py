from django.test import TestCase
from django.urls import reverse
from accounts.models import UserProfile
from api.tests import APISetupTests


class CoupleTests(APISetupTests, TestCase):

    def test_get_all_couples(self):

        # get all couples:
        final_response = self.client.get(
            self.LOCAL_HOST + reverse("get_all_couples"),
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )

        # were all the couples retrieved successfully?
        self.assertTrue(final_response.status_code == 200)
        self.assertTrue(len(list(final_response.json())), 2)

    def test_generate_code_for_partner(self):

        # generate a code for partner account linking
        code_response = self.client.get(
            self.LOCAL_HOST + reverse("generatecode"),
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        self.assertTrue(len(code_response.data["code"]), 5)

        # check that it was saved in the profile successfully
        my_profile = UserProfile.objects.get(
            user__email=self.main_user.data["email"])
        self.assertTrue(len(my_profile.account_linkage_code), 5)

    def test_input_code_and_link_accounts(self):

        # create user 1:
        self.client.post(
            self.LOCAL_HOST + reverse("sign_up"),
            data={
                "username": "leo",
                "email": "leo@gmail.com",
                "password": "HelloWorld1!",
            },
        )
        # create user 2:
        self.client.post(
            self.LOCAL_HOST + reverse("sign_up"),
            data={
                "username": "lyla",
                "email": "lyla@gmail.com",
                "password": "HelloWorld1!",
            },
        )
        # sign in as a leo:
        self.login_response = self.client.post(
            self.LOCAL_HOST + reverse("api-token-auth"),
            data={"username": "leo", "password": "HelloWorld1!"},
        )
        self.login_response = self.login_response.json()

        # generate a code for partner account linking as leo user:
        code_response = self.client.get(
            self.LOCAL_HOST + reverse("generatecode"),
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )

        # sign in as lyla:
        self.login_response = self.client.post(
            self.LOCAL_HOST + reverse("api-token-auth"),
            data={"username": "lyla", "password": "HelloWorld1!"},
        )
        self.login_response = self.login_response.json()

        # input the code to link accounts:
        response = self.client.get(
            self.LOCAL_HOST +
            reverse("inputcode", args=[code_response.data["code"]]),
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )

        self.assertEqual(response.data["success"], "Relationship Created!")

    def test_break_up(self):
        response = self.client.get(
            self.LOCAL_HOST + reverse("breakup"),
            HTTP_AUTHORIZATION="Token " + self.login_response["token"]
        )
        self.assertTrue(response.json()["limbo"])

    def test_cancel_break_up(self):
        response = self.client.get(
            self.LOCAL_HOST + reverse("cancelbreakup"),
            HTTP_AUTHORIZATION="Token " + self.login_response["token"]
        )
        self.assertFalse(response.json()["limbo"])
