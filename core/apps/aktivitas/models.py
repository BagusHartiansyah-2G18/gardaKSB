from django.db import models
from core.apps.accounts.User.models import User 

class AktivitasPegawai(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    judul = models.CharField(
        max_length=255
    )

    deskripsi = models.TextField()

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=11,
        decimal_places=8,
        null=True,
        blank=True
    )

    foto = models.ImageField(
        upload_to="aktivitas/",
        blank=True
    )

    tanggal_aktivitas = models.DateTimeField()