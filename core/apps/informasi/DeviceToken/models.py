from django.db import models

from core.apps.accounts.User.models import User


class DeviceToken(models.Model):

    PLATFORM_CHOICES = (
        ("ANDROID", "Android"),
        ("IOS", "iOS"),
        ("WEB", "Web"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="device_tokens"
    )

    token = models.TextField(
        unique=True
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True
    )

    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES
    )

    # is_active = models.BooleanField(
    #     default=True
    # )

    last_used_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    

    class Meta:
        verbose_name = "Device Token"
        verbose_name_plural = "Device Tokens"

    def __str__(self):
        return f"{self.user} - {self.platform}"