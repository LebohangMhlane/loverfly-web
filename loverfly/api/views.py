
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response
from accounts.models import UserProfile
from couples.models import Couple
from comments.models import Comment
from posts.models import Post

'''
This is intended for developing purposes only and should not
be included in final production. A better approach to this will
be implemented in the future.
For this to be valid:
DEBUG must be True
'''

@api_view(["GET"])
@permission_classes([])
def create_dummy_data(request, **kwargs):
    if settings.DEBUG:
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
            'Fury',
            'Regina',
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
        try:
            # create accounts for all the names above:
            for username in username_list:
                User.objects.create(username=username, password="poopypoop")
        except Exception as e:
            print(str(e))
            pass

        try:
            # get the user profiles:
            user_profiles = list(UserProfile.objects.all().exclude(username="kai"))
            # create couples for each pair of these users:
            index_starter = 0
            index_skipper = 1
            for index, user in enumerate(user_profiles):
                index = index + 1
                if index <= len(username_list) / 2:
                    # set partners:
                    partner_one = user_profiles[index_starter]
                    partner_two = user_profiles[user_profiles.index(partner_one) + index_skipper]
                    # set profile pictures:
                    partner_one.profile_picture = "https://image.tmdb.org/t/p/original/eZThh3UMkIcbZv6zs2lUSQlaBPF.jpg"
                    partner_two.profile_picture = "https://i.ytimg.com/vi/d3uIaw9NL8g/maxresdefault.jpg"
                    partner_one.save()
                    partner_two.save()
                    # create the couple:
                    Couple.objects.create(partner_one=partner_one, partner_two=partner_two)
                    # prepare the next couple:
                    index_starter = index_starter + 2
                else:
                    break
        except Exception as e:
            print(str(e))
            pass

        try:
            # create a post for each couple:
            couples = Couple.objects.all()
            for couple in couples:
                Post.objects.create(
                    couple=couple,
                    caption=str(couple.partner_one.username + ' + ' + couple.partner_two.username),
                    image="https://i.pinimg.com/originals/6c/7c/ce/6c7cce376c32532c7d503974d23a057f.jpg"
                )
                couple.has_posts = True
                couple.save()
        except Exception as e:
            print(e)
            pass

        try:
            create_dummy_comments()
        except Exception as e:
            print(str(e))
            pass

    return Response(status=200)

def create_dummy_comments():
    # get all the users:
    userprofiles = UserProfile.objects.all().exclude(username="kai")
    # create comments for every post:
    posts = Post.objects.all()
    for userprofile in userprofiles:
        for post in posts:
            Comment.objects.create(
                owner=userprofile,
                comment="This is a test comment from dummy data!",
                post=post
            )