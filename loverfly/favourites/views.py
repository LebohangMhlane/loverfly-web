from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

# from rest_framework.permissions import IsAdminUser, IsAuthenticated TODO: will activate later
from couples.models import Couple
from favourites.models import Fan
from couples.serializers import CoupleSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def favourite_a_couple(request, **kwargs):
    try:
        # do a sanity auth check before proceeding:
        if request.user.auth_token.key:
            my_profile = request.user.user
            couple = Couple.objects.get(id=kwargs["id"])

            # favourite or unfavourite:
            if kwargs["favourited"] == "false":
                _ = Fan.objects.create(
                    couple=couple,
                    fan=my_profile
                )
                my_profile.number_of_favourite_couples = my_profile.number_of_favourite_couples + 1
                my_profile.save()
                return Response({
                    "api_response": "Success",
                    "favourited": True
                })
            elif kwargs["favourited"] == "true":
                _ = Fan.objects.filter(
                    couple=couple,
                    fan=my_profile
                ).first().delete()
                my_profile.number_of_favourite_couples = my_profile.number_of_favourite_couples - 1
                my_profile.save()
                return Response({
                    "api_response": "Success",
                    "favourited": False
                })
    except Exception as e:
        return Response({
            "api_response": "failed",
            "error_info": str(e),
            "favourited": kwargs["favourited"]
        })


@api_view(["GET"])
@permission_classes([])
def get_favourited_couples(request, **kwargs):
    try:
        favourited_couples = []

        # get my favourited couples, paginated:
        pagination_object = PageNumberPagination()
        pagination_object.page_size = 10
        my_fan_objects = pagination_object.paginate_queryset(
            Fan.objects.filter(fan=request.user.user.id),
            request,
        )

        for fan_object in my_fan_objects:
            couple = CoupleSerializer(
                fan_object.couple,
                many=False)

            # add this couple to the favourited couples list:
            favourited_couples.append(couple.data)

        # return a dictionary containing favourited couple profiles and the count:
        return Response(
            {
                "api_response": "Success",
                "favourited_couples": favourited_couples,
                "number_of_favourited_couples": len(my_fan_objects),
                "next_page_link": pagination_object.get_next_link()
            }
        )
    except Exception as e:
        return Response(
            {
                "api_response": "Error",
                "favourited_couples": {},
                "number_of_favourited_couples": 0,
            }
        )


@api_view(["GET"])
@permission_classes([])
def check_if_couple_favourited(request, **kwargs):
    try:
        couple_favourited = Fan.objects.filter(couple__id=kwargs["couple_id"], fan=request.user.user).exists()
        return Response({
            "api_response": "success",
            "favourited": couple_favourited
        })
    except Exception as e:
        return Response({
            "api_response": "failed",
            "error_info": str(e),
            "favourited": False
        })

