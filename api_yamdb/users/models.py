from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = "admin"
MODERATOR = "moderator"
USER = "user"

CHOICES = (
    (ADMIN, "admin"),
    (MODERATOR, "moderator"),
    (USER, "user"),
)


class User(AbstractUser):
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=150,
        blank=False,
        unique=True
    )
    email = models.EmailField(
        verbose_name="Почта",
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
        null=True,
    )
    role = models.CharField(
        verbose_name="Статус",
        choices=CHOICES,
        default=USER,
        max_length=50,
    )
    confirmation_code = models.CharField(max_length=255)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
