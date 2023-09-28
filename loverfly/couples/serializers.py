
from rest_framework import serializers
from couples.models import Couple
from accounts.serializers import UserProfileSerializer

class CoupleSerializer(serializers.ModelSerializer):
    partner_one = UserProfileSerializer()
    partner_two = UserProfileSerializer()

    class Meta:
        model = Couple
        fields = "__all__"
        depth = 2
