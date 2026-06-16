from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .utils import MAX_PROFILE_PIC_SIZE


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

