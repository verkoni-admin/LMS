from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.exceptions import TokenError
from .utils import MAX_PROFILE_PIC_SIZE
from rest_framework_simplejwt.tokens import RefreshToken
from .models import InstructorProfile, MyUser


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

class UpdateInstructorProfile(serializers.ModelSerializer):

    class Meta:
        model = InstructorProfile

        fields = ["bio", "headline"]

class CommonUserAccountSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=8, write_only=True, required=False)
    new_password = serializers.CharField(min_length=8, write_only=True, required=False)
    confirm_password = serializers.CharField(min_length=8, write_only=True, required=False)

    class Meta:
        model = MyUser

        fields = ["name", "email", "old_password", "new_password", "confirm_password", "profile_pic"]


    def validate(self, attrs):
        password_fields = ["old_password", "new_password", "confirm_password"]
        # first check if the old_password entered by the user matches against the password stored in db
        # the instance is the MyUser instance passed into the serializer as first arg.
        user = self.instance

        if any(field in attrs for field in password_fields):
            if not attrs.get(password_fields[0]): raise serializers.ValidationError({"old_password": "old password is required"})
            if not attrs.get(password_fields[1]): raise serializers.ValidationError({"new_password": "new password is required"})
            if not attrs.get(password_fields[2]): raise serializers.ValidationError({"confirm_password": "confirm password is required"})

            if not user.check_password(attrs.get("old_password")):
                raise serializers.ValidationError({"old_password": "password is incorrect"})

            # check if the new password and the confirm password are correct!
            if attrs.get("new_password") != attrs.get("confirm_password"):
                raise serializers.ValidationError({"confirm_password": "passwords do not match"})

            # validate newpassword against user's email and name. so user doesn't enter like just their name as pass!
            validate_password(password=attrs.get("new_password"), user=user)

        return attrs

    def update(self, instance, validated_data):
        validated_data.pop("old_password", None)
        validated_data.pop("confirm_password", None)
        new_password = validated_data.pop("new_password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if new_password:
            instance.set_password(new_password)

        instance.save()

        return instance






