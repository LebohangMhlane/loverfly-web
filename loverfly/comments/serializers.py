
from rest_framework import serializers
from comments.models import Comment, CommentReply
from accounts.serializers import UserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer()

    class Meta:
        model = Comment
        fields = "__all__"
        depth = 2


class CommentReplySerializer(serializers.ModelSerializer):
    replier = UserProfileSerializer()

    class Meta:
        model = CommentReply
        fields = "__all__"
        depth = 1