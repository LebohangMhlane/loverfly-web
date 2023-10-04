from django.test import TestCase
from django.db.models import Q
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import reverse
from django.test import TestCase
from django.urls import reverse
from api.tests import APISetupTests
import requests

from couples.models import Couple
from posts.models import Post

class PostTests(APISetupTests, TestCase):

    def test_create_a_post(self):
        url = "https://machohairstyles.com/wp-content/uploads/2020/05/Chris-Hemsworth-Haircut_02-767x1024.jpg"
        response = requests.get(url)
        couple = Couple.objects.filter(
            Q(partner_one__id=self.main_user.data["id"]) | 
            Q(partner_two__id=self.main_user.data["id"])).first()
        data = {
            'image_name': "test_image",
            "image": SimpleUploadedFile("post-img-" + str(couple.id) + ".jpg", response.content),
            "caption": "caption"
        }
        response = self.client.post(
            self.LOCAL_HOST + reverse("create_a_post"),
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
            data=data
        )
        post = Post.objects.all().first()
        self.assertTrue(response.status_code, 200)

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
