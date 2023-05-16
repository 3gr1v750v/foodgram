from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Follow


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Отображение данных модели CustomUser."""

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
    search_fields = ("username", "email")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Отображение данных модели Follow (подписка на других пользователей).
    """

    list_display = (
        "user",
        "author",
    )
