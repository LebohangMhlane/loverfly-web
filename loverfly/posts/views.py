import datetime
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework.response import Response

from couples.models import Couple
from feed.views import prepare_post_data
from posts.models import Post
from posts.serializers import PostSerializer
from accounts.models import UserProfile

@api_view(["POST"])
@permission_classes([])
def create_a_post(request, **kwargs):
    try:
        # determine the couple:
        couple = Couple.objects.filter(Q(partner_one__user=request.user) | Q(
            partner_two__user=request.user)).first()

        # create the post:
        Post.objects.create(
            couple=couple,
            caption=request.data["caption"],
            image=request.data["image_url"],
        )

        couple.has_posts = True
        couple.save()
    except Exception as e:
        print(e)
        return Response({"error": "Failed to create the post"})
    return Response({"postcreated": True})


@api_view(["GET"])
@permission_classes([])
def get_couple_posts(request, **kwargs):
    try:
        # get the posts belonging to this couple:
        posts = Post.objects.filter(
            couple__id=kwargs["couple_id"], deleted=False,)
        serialized = PostSerializer(posts, many=True)
        return Response({
            "api_response": "Success",
            "couple_posts": serialized.data}
        )
    except Exception as e:
        return Response({
            "api_response": "Failed",
            "error_info": str(e)}
        )


@api_view(["POST"])
@permission_classes([])
def delete_post(request, **kwargs):
    try:
        # get the post:
        post = Post.objects.get(id=kwargs["post_id"])

        # this should only be allowed if the user couple matches the couple on the post (Some kind of lazy validation):
        if post.couple.partner_one.user == request.user or post.couple.partner_two.user == request.user:
            post.deleted = True
            post.deleted_date = datetime.datetime.now()
            post.save()

            # determine if this couple still has posts:
            posts = Post.objects.filter(
                Q(couple__partner_one__user=request.user) | Q(
                    couple__partner_two__user=request.user),
                deleted=False
            ).count()
            if not posts > 0:
                couple = Couple.objects.filter(id=post.couple.id).first()
                couple.has_posts = False
                couple.save()

        else:
            return Response({"post_deleted": False, "error": "The post does not belong to this users couple"})
        return Response({"post_deleted": True})

    except Exception as e:
        return Response({"post_deleted": False, "error": str(e)})


@api_view(["GET"])
@permission_classes([])
def view_single_post(request, **kwargs):
    try:
        my_profile = UserProfile.objects.get(user=request.user)
        post_id = kwargs["post_id"]
        post = Post.objects.filter(id=post_id).first()
        if post:
            post = PostSerializer(post, many=False)
            prepare_post_data(
                post=post,
                myprofile=my_profile,
                couple=post.couple
            )
            return Response({
                "api_response": "Success",
                "post": post.data
            })
        else:
            return Response({
                "api_response": "Not Found",
            })
    except Exception as e:
        return Response({
            "api_response": "Error"
        })
