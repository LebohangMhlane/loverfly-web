from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from couples.models import Couple
from posts.models import Post
from accounts.models import UserProfile
from likes.models import Liker


class APISetupTests(TestCase):
    LOCAL_HOST = "http://127.0.0.1:8000"

    def prepare_url(self, reversedendpoint, kwargs={}):
        url = self.LOCAL_HOST + \
            reverse(reversedendpoint, kwargs=kwargs if kwargs else None)
        return url

    def make_request(self, url="", data={}):
        response = self.client.post(
            url,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
            data=data if data else None
        )
        return response.json()

    def log_in_a_user(self, username, password):
        # log in a user:
        self.login_response = self.client.post(
            self.LOCAL_HOST + reverse("api-token-auth"),
            data={"username": "Kai", "password": "HelloWorld1!"},
        )
        self.login_response = self.login_response.json()
        # set the userprofile to self:
        self.user_profile = UserProfile.objects.get(user__id=self.main_user.data['id'])

    def create_a_user(self, username, email, password):
        # create a user:
        user_response = self.client.post(
            self.LOCAL_HOST + reverse("sign_up"),
            data={
                "username": username,
                "email": email,
                "password": password,
            },
        )
        return user_response

    def link_couple(self, partner_one, partner_two):
        partner_one = UserProfile.objects.get(
            id=partner_one.data["id"])
        partner_two = UserProfile.objects.get(
            id=partner_two.data["id"])
        partner_one.my_partner = partner_two
        partner_one.save()
        partner_two.my_partner = partner_one
        partner_two.save()
        self.couple_one = Couple.objects.create(
            partner_one=partner_one, partner_two=partner_two
        )

    def create_20_couples(self):
        username_list = [
            'Moe',
            'Johnny',
            'Abu',
            'Steve',
            'Saks',
            'Amy',
            'Marrisa',
            'Sne',
            'Zama',
            'Tony',
            'Anthony',
            'Macy',
            'Tina',
            'Lila',
            'Amaya',
            'Bella',
            'Edward',
            'Emma',
            'Felix',
            'Frank',
            'Obi',
            'Nica',
            'Male',
            'Female',
            'Ash',
            'Misty',
            'Fury'
            'Regina'
            'Fox',
            'Trot',
            'Timmy',
            'Tammy',
            'Lisa',
            'Scott',
            'Emily',
            'Tyler',
            'Sakhile',
            'Smangele',
            'Blade',
            'Rachel',
            'Neo',
            'Trinity',
        ]
        # create accounts for all the names above:
        for username in username_list:
            User.objects.create(username=username, password="poopypoop")
        # get the user profiles:
        user_profiles = list(UserProfile.objects.all())
        # create couples for each pair of these users:
        index_starter = 0
        index_skipper = 1
        for index, user in enumerate(user_profiles):
            index = index + 1
            if index <= len(username_list) / 2:
                partner_one = user_profiles[index_starter]
                partner_two = user_profiles[user_profiles.index(partner_one) + index_skipper]
                index_starter = index_starter + 2
                couple = Couple.objects.create(partner_one=partner_one, partner_two=partner_two)
            else:
                break
        # create a post for each couple:
        couples = Couple.objects.all()
        for couple in couples:
            Post.objects.create(
                couple=couple,
                caption=str(couple.partner_one.username + ' + ' + couple.partner_two.username),
                post_image="https://i.pinimg.com/originals/6c/7c/ce/6c7cce376c32532c7d503974d23a057f.jpg"
            )
            couple.has_posts = True
            couple.save()

    def setUp(self) -> None:

        # create more couples:
        self.create_20_couples()

        # create main user and userprofile:
        self.main_user = self.client.post(
            self.LOCAL_HOST + reverse("sign_up"),
            data={
                "username": "Kai",
                "email": "kai@gmail.com",
                "password": "HelloWorld1!",
            },
        )

        # log the main user in:
        self.log_in_a_user("Kai", "HelloWorld1!")

        # create user 1:
        create_user_1_response = self.create_a_user(
            "mikki", "mikki@gmail.com", "HelloWorld1!")

        # create user 2:
        create_user_2_response = self.client.post(
            self.LOCAL_HOST + reverse("sign_up"),
            data={
                "username": "lebo",
                "email": "lebo@gmail.com",
                "password": "HelloWorld1!",
            },
        )

        # create user 3:
        create_user_3_response = self.client.post(
            self.LOCAL_HOST + reverse("sign_up"),
            data={
                "username": "john",
                "email": "john@gmail.com",
                "password": "HelloWorld1!",
            },
        )

        # create user 4:
        create_user_4_response = self.client.post(
            self.LOCAL_HOST + reverse("sign_up"),
            data={
                "username": "jane",
                "email": "jane@gmail.com",
                "password": "HelloWorld1!",
            },
        )

        # link user 1 and 2 as a couple:
        self.link_couple(create_user_1_response, create_user_2_response)

        # create a post for couple 1:
        post = Post.objects.create(
            couple=self.couple_one,
            caption="Hello World Couple 1",
            post_image="myimage.jpg",
        )
        _ = Liker.objects.create(
            post=post, liker=UserProfile.objects.get(
                id=self.main_user.data["id"])
        )
        post.save()
        self.couple_one.has_posts = True
        self.couple_one.save()

        # link user main and 4 as a couple:
        partner_one = UserProfile.objects.get(id=self.main_user.data["id"])
        partner_two = UserProfile.objects.get(
            id=create_user_4_response.data["id"])
        self.couple_two = Couple.objects.create(
            partner_one=partner_one, partner_two=partner_two
        )
        partner_one.my_partner = partner_two
        partner_one.save()
        partner_two.my_partner = partner_one
        partner_two.save()

        # create a post for couple 2:
        post = Post.objects.create(
            couple=self.couple_two,
            caption="Hello World Couple 2",
            post_image="myimage.jpg",
        )
        _ = Liker.objects.create(
            post=post, liker=UserProfile.objects.get(
                id=self.main_user.data["id"])
        )
        post.save()
        self.couple_two.has_posts = True
        self.couple_two.save()

        # favourite this couple:
        favouriting_url = reverse(
            "favourite", kwargs={"id": 1, "admired": "false"})
        feed_page = self.client.get(
            path=favouriting_url,
            follow=True,
            HTTP_AUTHORIZATION="Token " + self.login_response["token"],
        )
        feed_page = feed_page.json()
        self.assertTrue(feed_page["admired"])

        return super().setUp()
