from django.test import TestCase
from django.urls import reverse
from api.tests import APISetupTests
from comments.models import Comment
from accounts.models import UserProfile
from posts.models import Post


class CommentTests(APISetupTests, TestCase):

    def test_comment_on_post(self):
        # post a comment:
        comment_data = {
            "user_profile_id": 1,
            "post_id": 1,
            "comment": "You guys are awesome together!"
        }
        url = reverse("post_comment", args=[1])
        api_response = self.client.post(
            self.LOCAL_HOST + url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
            data=comment_data
        )
        self.assertEqual(
            "Success",
            api_response.data["api_response"]
        )

    def test_get_comments(self):
        # post a comment:
        comment_data = {
            "user_profile_id": 1,
            "post_id": 1,
            "comment": "You guys are awesome together!"
        }
        url = reverse("post_comment", args=[1])
        api_response = self.client.post(
            self.LOCAL_HOST + url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
            data=comment_data
        )
        self.assertEqual(api_response.data["api_response"], "Success")

        url = reverse("get_comments", kwargs={"post_id": 1})
        api_response = self.client.get(
            self.LOCAL_HOST + url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
            data=comment_data
        )
        self.assertEqual(api_response.data["api_response"], "Success")

    def test_like_comment(self):
        profile = UserProfile.objects.get(id=self.main_user.data["id"])
        post = Post.objects.get(id=1)
        comment = Comment.objects.create(
            owner=profile,
            post=post,
            comment="This is a test comment"
        )
        # test like the comment:
        data = {
            "comment_id": comment.id,
            "comment_liked": "false"
        }
        url = reverse("like_comment")
        response = self.client.post(
            self.LOCAL_HOST + url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
            data=data
        )
        response = response.json()
        self.assertTrue(response["api_response"], "success")
        self.assertTrue(response["comment_liked"], True)

        # test unlike the comment:
        data["comment_liked"] = "true"
        response = self.client.post(
            self.LOCAL_HOST + url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
            data=data
        )
        response = response.json()
        self.assertTrue(response["api_response"], "success")
        self.assertFalse(response["comment_liked"], False)

    def test_delete_comment(self):
        comment = Comment.objects.create(
            owner=UserProfile.objects.get(id=self.main_user.data["id"]),
            comment="This is a test comment",
            post=Post.objects.get(id=1)
        )

        url = self.prepare_url("delete_comment", {"comment_id": comment.id})
        json_response = self.make_request(url)
        self.assertEqual(json_response["api_response"], "success")

        comment = Comment.objects.filter(id=comment.id)
        self.assertEqual(len(comment), 0)
