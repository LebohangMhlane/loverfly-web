from django.test import TestCase
from django.urls import reverse
from api.tests import APISetupTests
from comments.models import Comment, CommentReply
from accounts.models import UserProfile
from posts.models import Post


class CommentTests(APISetupTests, TestCase):

    def create_a_comment(self, optional_comment=None):
        # create a comment:
        comment_data = {
            "user_profile_id": 1,
            "post_id": 1,
            "comment": "You guys are awesome together!" if not optional_comment else optional_comment
        }
        url = reverse("post_comment", args=[1])
        response = self.client.post(
            self.LOCAL_HOST + url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
            data=comment_data
        )

    def reply_to_a_comment(self, optional_reply=None):
        self.create_a_comment()
        data = {
            "comment_id": 1,
            "reply": "This is a cool comment" if not optional_reply else optional_reply,
            "replier": 1,
        }
        url = reverse("reply_to_comment", kwargs={"comment_id": 1})
        response = self.client.post(
            url, data=data, HTTP_AUTHORIZATION="Token " + self.login_response["token"]
        )
        self.assertTrue(response.data["api_response"], "success")
        comment_reply = CommentReply.objects.all().first()
        self.assertTrue(comment_reply.comment_reply, "This is a cool comment")

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

    def test_create_comment_reply(self):
        self.create_a_comment()
        data = {
            "comment_id": 1,
            "reply": "This is a cool comment",
            "replier": 1,
        }
        url = reverse("reply_to_comment", kwargs={"comment_id": 1})
        response = self.client.post(
            url, data=data, HTTP_AUTHORIZATION="Token " + self.login_response["token"]
        )
        self.assertTrue(response.data["api_response"], "success")
        comment_reply = CommentReply.objects.all().first()
        self.assertTrue(comment_reply.comment_reply, "This is an optional comment")

        # create another comment reply for any errors:
        self.reply_to_a_comment(optional_reply="This is another reply")
        comment_replies = CommentReply.objects.all()
        comment_reply_one = comment_replies[0].comment_reply
        comment_reply_two = comment_replies[1].comment_reply
        self.assertEqual(len(comment_replies), 2)
        self.assertEqual(comment_reply_one, "This is a cool comment")
        self.assertEqual(comment_reply_two, "This is another reply")

    def test_get_comment_replies(self):
        self.create_a_comment()
        self.reply_to_a_comment()
        url = reverse("get_comment_replies", kwargs={"comment_id": 1})
        response = self.client.get(
            url, 
            HTTP_AUTHORIZATION="Token " + self.login_response["token"])
        self.assertTrue(response.data["api_response"], "success")
        self.assertTrue(len(response.data["comment_replies"]), 1)

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
