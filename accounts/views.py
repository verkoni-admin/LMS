from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import AllowAny
from accounts.serializers import RegisterUserSerializer, LoginUserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken

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

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginUserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data["user"]
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        response = Response({
            "id": user.id,
            "email": user.email,
            "profilePicUrl": user.profile_pic.url if user.profile_pic else None,
            "access_token": access_token,
        }, status=status.HTTP_200_OK)

        response.set_cookie(
            key="refresh_token",
            value=str(refresh_token),
            httponly=True,
            secure=True
        )

        return response

    return Response({
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


