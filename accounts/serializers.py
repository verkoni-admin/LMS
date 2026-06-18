from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.exceptions import TokenError
from .utils import MAX_PROFILE_PIC_SIZE
from rest_framework_simplejwt.tokens import RefreshToken
from .models import InstructorProfile


User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=["student", "instructor"],
        required=True
    )
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User

        fields = ["name", "email", "profile_pic", "role", "password", "confirm_password"]

    def validate_profile_pic(self, profile_pic_file):
        if profile_pic_file.size > MAX_PROFILE_PIC_SIZE:
            raise serializers.ValidationError({"profile_pic": f"profile pic file size should be less than {MAX_PROFILE_PIC_SIZE}"})
        return profile_pic_file

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "passwords do not match"})

        # validate against the user's email and name
        user = User(name=attrs["name"], email=attrs["email"])
        validate_password(password=attrs["password"], user=user)

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        print(validated_data)

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        if user.role == "instructor":
            # create the instructor profile
            InstructorProfile.objects.create(user=user)

        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError({"password": "Please check your credentials. Email or password is incorrect"})
        return password

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        try:
            user = User.objects.get(email=email)
            # case, the user does not exist in the database!
        except User.DoesNotExist:
            raise serializers.ValidationError({"password": "Please check your credentials. Email or password is incorrect"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Please check your credentials. Email or password is incorrect"})

        attrs["user"] = user

        return attrs

class RefreshJwtTokenSerializer(serializers.Serializer):

    def validate(self, attrs):
        request = self.context.get("request")
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            # make the user log in again! on frontend redirect!
            raise serializers.ValidationError("Refresh token does not exist. please log in again")

        try:
            token = RefreshToken(refresh_token)
            token.check_blacklist()
        except TokenError:
            raise serializers.ValidationError("Invalid or expired refresh token. Please log in again")

        user_id = token["user_id"]

        try:
            user = User.objects.get(id=user_id)
            attrs["user"] = user
            attrs["refresh_token"] = token
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        return attrs





