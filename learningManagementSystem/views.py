from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(["GET"])
def get_user(request):
    return Response({
        "message": "request was successful!",
        "user": {
            "name": request.user.name,
            "email": request.user.email,
            "profilePic": request.user.profile_pic.url
        },
        "is_authenticated": request.user.is_authenticated
    })


