from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import AllowAny
from accounts.serializers import RegisterUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterUserSerializer(data=request.data)
    print(request.FILES)

    if serializer.is_valid():
        user = serializer.save()

        return Response({
            "message": "user registered successfully",
            "user": {
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "profile_pic": user.profile_pic.url if user.profile_pic else None
            }
        }, status=status.HTTP_201_CREATED)

    return Response({
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)