
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from comments.models import Comment, CommentLike
from comments.serializers import CommentSerializer
from posts.models import Post
from accounts.models import UserProfile

@api_view(["POST"])
@permission_classes([])
def post_comment(request, **kwargs):
    try:
        post = Post.objects.get(id=kwargs["post_id"])
        comment_object = Comment.objects.create(
            owner=UserProfile.objects.get(user=request.user),
            comment=request.data["comment"],
            post=post
        )
        serialized_comment = CommentSerializer(comment_object, many=False)
        return Response({
            "api_response": "Success",
            "comment": serialized_comment.data
        })
    except Exception as e:
        return Response({
            "api_response": "Failed",
            "error_info": str(e)
        })


@api_view(["GET"])
@permission_classes([])
def get_comments(request, **kwargs):
    try:
        post_id = kwargs["post_id"]
        pagination_object = PageNumberPagination()
        pagination_object.page_size = 10
        results = pagination_object.paginate_queryset(
            Comment.objects.filter(post__id=post_id).order_by("id"),
            request,
        )
        serialized_comments = CommentSerializer(results, many=True)
        comments = []
        for comment in serialized_comments.data:
            comments.append({
                "comment_liked": CommentLike.objects.filter(
                    owner__user=request.user, comment=comment["id"]
                ).exists(),
                "comment": comment,
            })
        next_page_link = pagination_object.get_next_link()
        return Response({
            "api_response": "Success",
            "comments": comments,
            "next_page_link": next_page_link,
            "results_end_reached": False
        })
    except Exception as e:
        return Response({
            "api_response": "Fail",
            "comments": [],
            "error_info": str(e)
        })


@api_view(["POST"])
@permission_classes([])
def like_comment(request, **kwargs):
    try:
        comment_data = request.data
        comment = Comment.objects.get(id=comment_data["comment_id"])
        if comment_data["comment_liked"] == "false":
            comment_like = CommentLike.objects.create(
                owner=request.user.user,
                comment=comment
            )
            if comment_like:
                comment.comment_likes += 1
                comment.save()
                return Response({
                    "api_response": "success",
                    "comment_liked": True
                })
        else:
            CommentLike.objects.get(
                comment=comment, owner=request.user.user).delete()
            comment.comment_likes -= 1
            comment.save()
            return Response({
                "api_response": "success",
                "comment_liked": False
            })
    except Exception as e:
        return Response({
            "api_response": "failed",
            "error_info": str(e),
        })


@api_view(["POST"])
@permission_classes([])
def delete_comment(request, **kwargs):
    try:
        # get the comment:
        comment_id = kwargs["comment_id"]
        comment = Comment.objects.get(id=comment_id)

        # delete the comment likes:
        CommentLike.objects.filter(comment=comment).delete()
        comment.delete()
        return Response({
            "api_response": "success",
        })
    except Exception as e:
        return Response({
            "api_response": "failed",
            "error_info": str(e),
        })
