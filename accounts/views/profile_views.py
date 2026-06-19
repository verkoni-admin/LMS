from rest_framework.decorators import api_view, permission_classes
from ..serializers import UpdateInstructorProfile, CommonUserAccountSerializer
from rest_framework.permissions import IsAuthenticated
from ..models import InstructorProfile
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

@api_view(["POST", "PATCH", "PUT"])
@permission_classes([IsAuthenticated])
def update_instructor_profile(request):
    user = request.user
    if not user.role == "instructor":
        print("user is not an instructor")
        raise

    instructor_profile = InstructorProfile.objects.get(user=user)
    serializer = UpdateInstructorProfile(instructor_profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "updated profile successfully",
        }, status=status.HTTP_200_OK)

    return Response({
        "errors": serializer.errors
    }, status.HTTP_400_BAD_REQUEST)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def base_profile(request):
    user_profile = request.user
    serializer = CommonUserAccountSerializer(user_profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Profile updated successfully",
            "name": user_profile.name,
            "email": user_profile.email,
            "profile_pic": user_profile.profile_pic.url if user_profile.profile_pic else None,
            "role": user_profile.role
        }, status.HTTP_200_OK)

    return Response({
        "errors": serializer.errors
    }, status.HTTP_400_BAD_REQUEST)

