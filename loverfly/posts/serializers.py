
from rest_framework import serializers

from couples.serializers import CoupleSerializer
from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    couple = CoupleSerializer()

    class Meta:
        model = Post
        fields = "__all__"
