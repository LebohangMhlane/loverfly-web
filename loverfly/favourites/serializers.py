
from rest_framework import serializers

from accounts.serializers import UserProfileSerializer
from favourites.models import Admirer

class AdmirerSerializer(serializers.ModelSerializer):
    admirer = UserProfileSerializer()
    class Meta:
        model = Admirer
        fields = ["admirer"]
        # enables self serialization of fields that relate to itself (Very useful)
        depth = 1