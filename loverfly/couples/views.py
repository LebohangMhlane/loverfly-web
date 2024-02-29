import datetime

from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import shortuuid

from couples.models import Couple
from couples.serializers import CoupleSerializer
from accounts.models import UserProfile
from admirers.models import Admirer

@api_view(["GET"])
@permission_classes([])
def get_couple(request, **kwargs):

    # see if we can find the couple:
    couple = Couple.objects.filter(id=kwargs["couple_id"]).first()

    # am i admiring this couple:
    is_admired = Admirer.objects.filter(
        admirer=request.user.user, 
        couple=couple
    ).exists()

    # if a couple is found then retun it serialized:
    if couple:
        couple_serialized = CoupleSerializer(couple, many=False)
        return Response({
            "couple": couple_serialized.data,
            "isAdmired": is_admired
        })
    else:
        return Response({"error": "A couple with this ID was not found"})


@api_view(["GET"])
@permission_classes([])
def generate_code_for_partner(request, **kwargs):
    code = ""
    try:
        my_profile = UserProfile.objects.get(user=request.user)
        code = shortuuid.uuid()[0:5]
        my_profile.account_linkage_code = code
        my_profile.save()
    except Exception as e:
        return {"error": "Failed to generate code!"}
    return Response({"code": code})


@api_view(["GET"])
@permission_classes([])
def input_code_and_link_accounts(request, **kwargs):
    try:
        code = kwargs["code"]
        my_profile = UserProfile.objects.get(user=request.user)
        partner_profile = UserProfile.objects.filter(
            account_linkage_code=code).first()

        # ensure partner is single:
        if partner_profile:
            if partner_profile.my_partner:
                return Response({"error": "This person is not single!"})
            else:

                # link accounts as a new couple:
                Couple.objects.create(
                    partner_one=my_profile,
                    partner_two=partner_profile
                )

                # set partner data:
                my_profile.my_partner = partner_profile
                my_profile.save()
                partner_profile.my_partner = my_profile
                partner_profile.save()
        else:
            return Response({
                "error": "A partner with this code doesn't exist! Have your partner Generate a Code then come back here and try again!"
            })
        return Response({
            "success": "Relationship Created!"
        })
    except Exception as e:
        return Response({
            "error": "failed to create the relationship"
        })


@api_view(["GET"])
@permission_classes([])
def break_up(request, **kwargs):
    try:
        couple = Couple.objects.get(
            Q(partner_one__user=request.user) | Q(
                partner_two__user=request.user)
        )
        couple.limbo = True
        couple.is_active = False
        couple.limbo_date = datetime.datetime.now()
        couple.save()
        return Response({"limbo": True})
    except Exception as e:
        return Response({"error": str(e)})


@api_view(["GET"])
@permission_classes([])
def cancel_break_up(request, **kwargs):
    try:
        couple = Couple.objects.get(
            Q(partner_one__user=request.user) | Q(
                partner_two__user=request.user)
        )
        couple.limbo = False
        couple.is_active = True
        couple.save()
        return Response({"limbo": False})
    except Exception as e:
        return Response({"error": str(e)})
