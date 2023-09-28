from django.test import TestCase
from rest_framework import reverse
from django.test import TestCase
from django.urls import reverse
from api.tests import APISetupTests


class PostTests(APISetupTests, TestCase):

    def test_create_a_post(self):
        data = {
            "image_url": "image_url",
            "caption": "caption"
        }
        response = self.client.post(
            self.LOCAL_HOST + reverse("create_a_post"),
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
            data=data
        )
        self.assertTrue(response.json()["postcreated"])

    def test_delete_post(self):

        # sign in as mikki:
        self.login_response = self.client.post(
            self.LOCAL_HOST + reverse("api-token-auth"),
            data={"username": "mikki", "password": "HelloWorld1!"},
        )
        self.login_response = self.login_response.json()

        # get the posts mikki's couple has created:
        url = reverse("get_couple_posts", kwargs={
                      "couple_id": self.couple_one.id})
        response = self.client.get(
            self.LOCAL_HOST + url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )

        # set the post to deleted state:
        url = reverse("delete_post", kwargs={
                      "post_id": response.json()["couple_posts"][0]["id"]})
        response = self.client.post(
            self.LOCAL_HOST + url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        self.assertTrue(response.json()["post_deleted"])

    def test_get_couple_posts(self):

        # sign in as mikki:
        self.login_response = self.client.post(
            self.LOCAL_HOST + reverse("api-token-auth"),
            data={"username": "mikki", "password": "HelloWorld1!"},
        )
        self.login_response = self.login_response.json()

        # get the posts mikki's couple has created:
        url = reverse("get_couple_posts", kwargs={
                      "couple_id": self.couple_one.id})
        response = self.client.get(
            self.LOCAL_HOST + url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        post_length = len(response.json()["couple_posts"])
        self.assertTrue(post_length, 1)

    def test_view_single_post(self):

        # view a single post and all it's required data:
        url = reverse("view_single_post", kwargs={"post_id": 1})
        api_response = self.client.get(
            self.LOCAL_HOST + url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        self.assertTrue(api_response.data["api_response"], "Success")
