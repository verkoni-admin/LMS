from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from accounts.validators import validate_image_size
from django.core.exceptions import ValidationError

# Create your models here.

# my custom user model
class CustomAuthUserManager(BaseUserManager):
    def create_user(self, email, password, name, role="student", **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, role=role, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, password=password, name=name)
        user.is_staff = True
        user.is_superuser = True
        user.role = "Admin"
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
        default="student",
        null=True,
        blank=True
    )
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profiles/", validators=[validate_image_size])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # define the manager
    objects = CustomAuthUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["name"]


class InstructorProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    headline = models.CharField(max_length=300, null=True)
    bio = models.TextField(null=True)
    # run migrations!

    def __str__(self):
        return self.user.name

    def clean(self):
        if self.user.role != "instructor":
            print("Model Level: user is not an instructor")
            raise ValidationError("User is not an instructor")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
