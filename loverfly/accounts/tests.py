from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import requests

from accounts.models import ProfilePicture, UserProfile
from api.tests import APISetupTests


class AccountsTest(APISetupTests, TestCase):

    def test_sign_up(self):
        # create the user:
        response = self.client.post(
            self.LOCAL_HOST + reverse("sign_up"),
            data={
                "username": "Johnny",
                "email": "johnny@gmail.com",
                "password": "HelloWorld1!",
            },
        )
        # get the user profile
        userprofile = UserProfile.objects.get(username="Johnny")
        # was the user created in successfully ?
        self.assertTrue(response.status_code == 200)
        # was the userprofile created successfully ?
        self.assertTrue(userprofile.username == "Johnny")

    def test_get_user_profile(self):

        # create and log the user in:
        response = self.client.post(
            self.LOCAL_HOST + reverse("sign_up"),
            data={
                "username": "Lebby",
                "email": "lebby@gmail.com",
                "password": "HelloWorld1!",
            },
        )

        # sign in as Lebby:
        self.login_response = self.client.post(
            self.LOCAL_HOST + reverse("api-token-auth"),
            data={"username": "Lebby", "password": "HelloWorld1!"},
        )
        self.login_response = self.login_response.json()

        # get the user profile:
        response = self.client.post(
            self.LOCAL_HOST + reverse("get_user_profile_and_couple_data"),
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )

        # was the user profile retrieved successfully ?
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(list(response)), 1)

    def test_get_all_users(self):

        # get all users
        response = self.client.get(
            self.LOCAL_HOST + reverse("get_all_users"),
        )

        # were the users retrieved successfully?
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(response.data), 5)

    def test_get_api_token_and_user_profile(self):

        # get an api token:
        response = self.client.post(
            self.LOCAL_HOST + reverse("api-token-auth"),
            data={"username": "mikki", "password": "HelloWorld1!"},
        )

        # was the user logged in successfully:
        self.assertTrue(response.status_code == 200)
        self.assertContains(response, "token")

    def test_update_profile_picture(self):
        url = "https://machohairstyles.com/wp-content/uploads/2020/05/Chris-Hemsworth-Haircut_02-767x1024.jpg"
        response = requests.get(url)
        data = {
            "image": SimpleUploadedFile("profilepicture.jpg", response.content),
        }
        response = self.client.post(
            self.LOCAL_HOST + reverse("update_profile_picture"),
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
            data=data
        )
        profile_picture = ProfilePicture.objects.all().first()
        self.assertEqual(profile_picture.image.name, "profile_pictures/41")
        self.assertTrue(response.status_code, 200)
