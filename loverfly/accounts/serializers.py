
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from accounts.models import ProfilePicture, UserProfile, UserSetting


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        # create the user object:
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=make_password(validated_data["password"]),
        )
        user_profile = UserProfile.objects.get(user=user)
        user_settings = UserSetting.objects.create(
            user_profile=user_profile
        )
        return user_profile

class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ["image"]
        depth = 2

class UserProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    profile_picture = ProfilePictureSerializer()

    class Meta:
        model = UserProfile
        fields = "__all__"
        # enables self serialization of fields that relate to itself (Very useful)
        depth = 2


class UserSettingSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model = UserSetting()
        fields = "__all__"
        depth = 2
