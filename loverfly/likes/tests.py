from django.test import TestCase
from django.urls import reverse

from likes.models import Liker
from posts.models import Post
from api.tests import APISetupTests


class LikeTests(APISetupTests, TestCase):

    def test_like_unlike_a_post(self):
        # the post should have zero likes:
        post = Post.objects.get(id=1)
        self.assertEqual(post.likes, 0)

        # like the post:
        url = reverse("like_post", kwargs={"post_id": 1, "post_liked": "false"})
        api_response = self.client.get(
            self.LOCAL_HOST + url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        self.assertEqual(api_response.data["api_response"], "Success")

        # the post should have one like:
        post = Post.objects.get(id=1)
        self.assertEqual(post.likes, 1)

        # the post should now be liked:
        likers = Liker.objects.filter(post__id=1)
        self.assertEqual(len(likers), 1)

        # unlike the post:
        url = reverse("like_post", kwargs={
                      "post_id": 1, "post_liked": "true"})
        api_response = self.client.get(
            self.LOCAL_HOST + url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        self.assertEqual(api_response.data["api_response"], "Success")

        # this post should be unliked by us:
        likers = Liker.objects.filter(post__id=1)
        self.assertEqual(len(likers), 0)

        # the post should have zero likes:
        post = Post.objects.get(id=1)
        self.assertEqual(post.likes, 0)
