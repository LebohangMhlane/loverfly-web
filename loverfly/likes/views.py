from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from likes.models import Liker
from posts.models import Post
from accounts.models import UserProfile

@api_view(["GET"])
@permission_classes([])
def like_a_post(request, **kwargs):
    post_liked = False
    my_profile = UserProfile.objects.get(user__username=request.user.username)
    try:
        post = Post.objects.get(id=kwargs["post_id"])
        if kwargs["post_liked"] == "true":
            _ = Liker.objects.filter(
                liker=my_profile, post=post).first().delete()
            post_liked = False
        elif kwargs["post_liked"] == "false":
            if not Liker.objects.filter(
                liker=my_profile, post=post).exists():
                _ = Liker.objects.create(
                    liker=my_profile,
                    post=post,
                )
                post_liked = True
            else:
                post_liked = True
        return Response({
            "api_response": 'Success',
            "post_liked": post_liked
        })
    except Exception as e:
        return Response({
            "api_response": 'An error occured while liking this post',
        })
