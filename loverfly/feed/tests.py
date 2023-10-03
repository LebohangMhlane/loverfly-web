from django.test import TestCase
from django.urls import reverse

from api.tests import APISetupTests


class FeedTests(APISetupTests, TestCase):

    def test_get_posts_for_feed(self):

        # load the post feed page:
        feed_page = self.client.get(
            path=reverse("get_posts_for_feed"),
            follow=True,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        feed_page = feed_page.json()

        # test checks
        self.assertEqual(len(feed_page["posts"]), 2)
        self.assertEqual(feed_page["posts"][0]["couple"]
                         ["partner_one"]["username"], "Kai")
