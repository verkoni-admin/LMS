from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.

# my custom user model
class CustomAuthUserManager(BaseUserManager):
    def create_user(self, email, password, name):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, password=password, name=name)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("instructor", "Instructor")
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    # here the roles should be choices field ig
    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        default="student"
    )
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profiles/")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # define the manager
    objects = CustomAuthUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["name"]

