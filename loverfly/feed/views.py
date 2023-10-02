from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# from rest_framework.permissions import IsAdminUser, IsAuthenticated TODO: will activate later
from couples.serializers import CoupleSerializer

from admirers.models import Admirer
from likes.models import Liker
from posts.models import Post
from posts.serializers import PostSerializer

# Create your views here.

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_posts_for_feed(request, **kwargs):
    try:
        """
        returns one latest post for all admired couples
        to populate the home feed page
        """
        all_posts = {"posts": []}

        # get my favourite couples (paginated):
        pagination_object = PageNumberPagination()
        pagination_object.page_size = 5
        paginated_admirer_objects = pagination_object.paginate_queryset(
            Admirer.objects.filter(admirer__user=request.user).order_by("id"),
            request
        )

        # get the post for each admired user and prepare the data:
        for admirer_object in paginated_admirer_objects:
            if admirer_object.couple.has_posts:
                couples_latest_post = Post.objects.filter(
                    couple=admirer_object.couple, deleted=False
                ).latest()
                if couples_latest_post:
                    post_data = prepare_post_data(
                        couples_latest_post,
                        request.user,
                        admirer_object.couple
                    )
                    all_posts["posts"].append(post_data)

        # return pagination data so we can prep our next request:
        all_posts["pagination_link"] = pagination_object.get_next_link()

        return Response(all_posts)
    except Exception as e:
        print(e)
        return Response({
            "error": "error",
            "error_info": str(e)
        })


def prepare_post_data(post, current_user, couple):
    is_liked = Liker.objects.filter(
        post=post, liker__user=current_user).exists()
    is_admired = Admirer.objects.filter(admirer__user=current_user).exists()
    post_data = {
        "isLiked": is_liked,
        "isAdmired": is_admired,
        "post": PostSerializer(post, many=False).data,
        "couple": CoupleSerializer(couple, many=False).data
    }
    return post_data
