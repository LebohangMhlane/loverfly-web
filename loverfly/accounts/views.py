
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes

# from rest_framework.permissions import IsAdminUser, IsAuthenticated TODO: will activate later
from django.db.models import Q
from django.contrib.auth.models import User

from couples.models import Couple
from couples.serializers import CoupleSerializer
from .models import ProfilePicture, UserProfile
from .serializers import ProfilePictureSerializer, UserProfileSerializer, UserSerializer


@api_view(["POST"])
@permission_classes([])
def sign_up(request):
    user_serializer = UserSerializer(data=request.data)
    try:
        if user_serializer.is_valid(raise_exception=True):
            user_profile = user_serializer.create(validated_data=request.data)
            user_profile = UserProfileSerializer(user_profile, many=False)
            return Response(user_profile.data, status=201)
    except serializers.ValidationError as e:
        return Response({"error": True, "error_msg": str(e.detail["username"][0])})


@api_view(["GET"])
@permission_classes([])
def get_all_users(request):
    response = User.objects.all()
    serializer = UserSerializer(response, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([])
def get_user_profile_and_couple_data(request, **kwargs):

    # get the user profile:
    profile = UserProfile.objects.get(user=request.user)
    profile_serialized = UserProfileSerializer(profile, many=False)

    # if this user is in a relationship, return the couple as well:
    couple = Couple.objects.filter(
        Q(partner_one__user=request.user) |
        Q(partner_two__user=request.user)).first()
    if couple:
        couple_serialized = CoupleSerializer(couple, many=False)
        return Response({
            "user_profile": profile_serialized.data,
            "couple": couple_serialized.data,
        })
    return Response({
        "user_profile": profile_serialized.data,
        "couple": {},
    })


@api_view(["POST"])
@permission_classes([])
def update_profile_picture(request, **kwargs):
    try:
        # there should be one already created:
        profile_picture = ProfilePicture.objects.filter(user_profile=request.user.user)
        if profile_picture:
            profile_picture = profile_picture.first()
            profile_picture.image = request.data["image"]
            profile_picture.save()
            serialized = ProfilePictureSerializer(profile_picture, many=False)
            return Response({
                "profile_picture": serialized.data,
            })
        else:
            profile_picture = ProfilePicture()
            profile_picture.user_profile = request.user.user
            profile_picture.image = request.data["image"]
            profile_picture.save()
            serialized = ProfilePictureSerializer(profile_picture, many=False)
            return Response({
                "profile_picture": serialized.data,
            })
    except Exception as e:
        return Response({
            "error": "something went wrong",
            "error_info": str(e)
        })