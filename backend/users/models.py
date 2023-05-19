from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

from .validators import (
    username_name_list_validator,
    username_pattern_validation,
)


class CustomUser(AbstractUser):
    """Модель пользователя."""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        "username",
        "first_name",
        "last_name",
    )

    username = models.CharField(
        verbose_name="Юзернейм",
        help_text=(
            f"""Введите юзернейм пользователя 
            (не более {settings.DEFAULT_MAX_LENGTH} символов)"""
        ),
        max_length=settings.DEFAULT_MAX_LENGTH,
        unique=True,
        validators=[username_pattern_validation, username_name_list_validator],
        error_messages={"unique": settings.UNIQUE_USERNAME},
    )
    email = models.EmailField(
        verbose_name="Электронный почтовый адрес",
        help_text=(
            f"""Введите электронный почтовый адрес 
            (не более {settings.EMAIL_MAX_LENGTH} символов)"""
        ),
        unique=True,
        max_length=settings.EMAIL_MAX_LENGTH,
        error_messages={"unique": settings.UNIQUE_EMAIL},
    )
    password = models.CharField(
        verbose_name="Пароль",
        help_text=(
            f"""Придумайте пароль 
            (не более {settings.DEFAULT_MAX_LENGTH} символов)"""
        ),
        max_length=settings.DEFAULT_MAX_LENGTH,
    )
    first_name = models.CharField(
        verbose_name="Имя пользователя",
        help_text=(
            f"""Введите имя пользователя 
            (не более {settings.DEFAULT_MAX_LENGTH} символов)"""
        ),
        max_length=settings.DEFAULT_MAX_LENGTH,
    )

    last_name = models.CharField(
        verbose_name="Фамилия пользователя",
        help_text=(
            f"""Введите фамилию пользователя 
            (не более {settings.DEFAULT_MAX_LENGTH} символов)"""
        ),
        max_length=settings.DEFAULT_MAX_LENGTH,
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ("-id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Follow(models.Model):
    """
    Модель подписок на других пользователей (авторов).
    Ограничения:
    - Пользователь не может быть подписан сам на себя.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Пользователь",
    )

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Подписан на автора",
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "Подписка на автора"
        verbose_name_plural = "Подписки на авторов"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"], name="unique_user_author"
            ),
            models.CheckConstraint(
                check=~models.Q(author=models.F("user")), name="no_self_follow"
            ),
        ]

    def __str__(self):
        return f"Пользователь {self.user} подписан на {self.author}"
