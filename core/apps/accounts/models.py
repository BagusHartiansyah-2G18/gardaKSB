from django.db import models
from django.conf import settings

from core.apps.master.Desa.models import Desa 
from core.apps.master.Bidang.models import Bidang 

class UserProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    alamat = models.TextField(
        blank=True
    )

    desa = models.ForeignKey(
        Desa,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    bidang = models.ForeignKey(
        Bidang,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    foto = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    last_latitude = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True
    )

    last_longitude = models.DecimalField(
        max_digits=11,
        decimal_places=8,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username