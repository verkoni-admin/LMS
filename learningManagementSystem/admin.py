from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(MyUser)
class UserAdmin(UserAdmin):
    model = MyUser

    list_display = ("name", "role", "email", "profile_pic", "is_active", "is_staff")
    list_filter = ("is_staff", "is_active", "is_superuser", "role")
    search_fields = ("email", "name")
    ordering = ("email",)
    list_display_links = ("name", "email")

    fieldsets = (
        ("Login Info", {
            "fields": ("email", "password")
        }),

        ("Personal Info", {
            "fields": ("name", "profile_pic", "role")
        }),

        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),

        ("Important Dates", {
            "fields": ("last_login",)
        })

    )

    add_fieldsets = (
        ("Create User", {
            "classes": ("wide",),
            "fields": ("email", "name", "role", "password1", "profile_pic", "password2", "is_staff", "is_active")
        }),
    )

    readonly_fields = (
        "created_at",
        "last_login",
        "updated_at"
    )


