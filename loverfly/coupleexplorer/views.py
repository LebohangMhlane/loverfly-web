from operator import itemgetter
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q

from couples.models import Couple
from couples.serializers import CoupleSerializer
from admirers.models import Admirer
from posts.models import Post

@api_view(["GET"])
@permission_classes([])
def get_trending_couples(request):
    try:
        couples = Couple.objects.filter(
            ~Q(Q(partner_one__user=request.user) |
                Q(partner_two__user=request.user))
        )[:10]

        trending_couples = []
        for couple in couples:
            couple_posts = Post.objects.filter(couple=couple).values("likes")

            total_post_likes = 0
            for like_count in couple_posts:
                total_post_likes = total_post_likes + like_count["likes"]

            couple_data = {}
            isAdmired = Admirer.objects.filter(admirer__user=request.user, couple=couple).exists()
            serialized_couple = CoupleSerializer(couple, many=False)

            couple_data["total_post_likes"] = total_post_likes
            couple_data["couple"] = serialized_couple.data
            couple_data["isAdmired"] = isAdmired
            trending_couples.append(couple_data)

        trending_couples = sorted(
            trending_couples, key=itemgetter("total_post_likes"), reverse=True
        )
        return Response({
            "api_response": "Successful",
            "trending_couples": trending_couples
        })
    except Exception as e:
        return Response({
            "api_response": "Fail",
            "trending_couples": [],
            "error_info": str(e)
        })


@api_view(["GET"])
@permission_classes([])
def get_all_couples(request):  # TODO: Will need to implement pagination:
    try:
        couples = Couple.objects.filter(
            ~Q(Q(partner_one__user=request.user) |
               Q(partner_two__user=request.user))
        )
        # =========================
        # prepare the couples data:
        # =========================
        all_couples = []
        for couple in couples:
            couple_data = {}

            # is the couple admired:
            is_favourited = False
            if Admirer.objects.filter(
                    admirer__user=request.user,
                    couple=couple).exists():
                is_favourited = True

            serialized_couple = CoupleSerializer(couple, many=False)
            couple_data["couple"] = serialized_couple.data
            couple_data["isAdmired"] = is_favourited
            all_couples.append(couple_data)
        return Response({
            "apiResponse": "Successful",
            "couples": all_couples,
        })
    except Exception as e:
        return Response({
            "apiResponse": "Fail",
            "couples": [],
            "ErrorInfo": str(e)
        })
