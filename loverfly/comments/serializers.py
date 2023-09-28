
from rest_framework import serializers
from comments.models import Comment
from accounts.serializers import UserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer()

    class Meta:
        model = Comment
        fields = "__all__"
        depth = 2
