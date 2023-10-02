from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

# from rest_framework.permissions import IsAdminUser, IsAuthenticated TODO: will activate later
from couples.models import Couple
from favourites.models import Admirer
from couples.serializers import CoupleSerializer
from favourites.serializers import AdmirerSerializer

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
                _ = Admirer.objects.create(
                    couple=couple,
                    admirer=my_profile
                )
                my_profile.number_of_favourite_couples = my_profile.number_of_favourite_couples + 1
                my_profile.save()
                return Response({
                    "api_response": "Success",
                    "favourited": True
                })
            elif kwargs["favourited"] == "true":
                _ = Admirer.objects.filter(
                    couple=couple,
                    admirer=my_profile
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
        admirer = pagination_object.paginate_queryset(
            Admirer.objects.filter(admirer=request.user.user.id),
            request,
        )

        for admirer_object in admirer:
            couple = CoupleSerializer(
                admirer_object.couple,
                many=False)

            # add this couple to the favourited couples list:
            favourited_couples.append(couple.data)

        # return a dictionary containing favourited couple profiles and the count:
        return Response(
            {
                "api_response": "Success",
                "favourited_couples": favourited_couples,
                "number_of_favourited_couples": len(admirer),
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
def get_all_admirers(request, **kwargs):
    try:
        # get all my admirers, paginate by 14:
        pagination_object = PageNumberPagination()
        pagination_object.page_size = 14
        my_couple = Couple.objects.filter(
            Q(partner_one__username=request.user.user.username) | 
              Q(partner_two__username=request.user.user.username)).first()
        my_admirers = pagination_object.paginate_queryset(
            Admirer.objects.filter(couple=my_couple),
            request,
        )
        # prepare the admirers response data:
        serialized_admirers = AdmirerSerializer(my_admirers, many=True)
        return Response(
            {"api_response": "success",
            "admirers": serialized_admirers.data,
            "next_page_link": pagination_object.get_next_link()
            }
    )
    except Exception as e:
        return {"api_response": "failed",
                "admirers": {},
                "next_page_link": pagination_object.get_next_link()
                }   


@api_view(["GET"])
@permission_classes([])
def check_if_couple_favourited(request, **kwargs):
    try:
        couple_favourited = Admirer.objects.filter(couple__id=kwargs["couple_id"], admirer=request.user.user).exists()
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

