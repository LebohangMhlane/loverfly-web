
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from comments.models import Comment, CommentLike, CommentReply, CommentReplyLike
from comments.serializers import CommentReplySerializer, CommentSerializer
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
            if not CommentLike.objects.filter(owner=request.user.user, comment=comment.id).exists():
                CommentLike.objects.create(
                    owner=request.user.user,
                    comment=comment
                )
                comment.save()
                return Response({
                    "api_response": "success",
                    "comment_liked": True
                })
            else:
                 return Response({
                    "api_response": "success",
                    "comment_liked": True
                })
        else:
            CommentLike.objects.get(
                comment=comment, owner=request.user.user).delete()
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


@api_view(["GET"])
@permission_classes([])
def get_comment_replies(request, **kwargs):
    comment_replies = []
    try:
        replies = CommentReply.objects.filter(comment_replied_to__id=kwargs["comment_id"])
        comment_replies_serialized = CommentReplySerializer(replies, many=True)
        for reply in comment_replies_serialized.data:
            my_profile = request.user.user
            if CommentReplyLike.objects.filter(comment_reply__id=reply["id"], liker=my_profile).exists():
                reply_data = {
                    "comment_liked": True,
                    "comment_reply": reply,
                    "comment_reply_likes": CommentReplyLike.objects.filter(comment_reply__id=reply["id"]).count()
                }
                comment_replies.append(reply_data)
            else:
                reply_data = {
                    "comment_liked": False,
                    "comment_reply": reply,
                    "comment_reply_likes": CommentReplyLike.objects.filter(comment_reply__id=reply["id"]).count()
                }
                comment_replies.append(reply_data)
        return Response({
            "api_response": "success",
            "comment_replies": comment_replies
        })
    except Exception as e:
        return Response({
            "api_response": "failed",
            "error_info": str(e),
        })


@api_view(["POST"])
@permission_classes([])
def reply_to_comment(request, **kwargs):
    try:
        my_profile = request.user.user
        comment_data = request.data
        comment = Comment.objects.filter(id=int(comment_data["comment_id"])).first()

        if comment:
            comment_reply = CommentReply()
            comment_reply.comment_replied_to = comment
            comment_reply.replier = my_profile
            comment_reply.comment_reply = comment_data["comment"]
            comment_reply.save()
            comment_reply_serialized = CommentReplySerializer(comment_reply, many=False)
        return Response({
            "api_response": "success",
            "comment_reply": {
                    "comment_liked": False,
                    "comment_reply": comment_reply_serialized.data,
                    "comment_reply_likes": 0
                },
        })
    except Exception as e:
        return Response({
            "api_response": "failed",
            "error_info": str(e)
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
