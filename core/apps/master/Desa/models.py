from django.db import models
from core.apps.master.models import Kecamatan 

class Desa(models.Model):
    kecamatan = models.ForeignKey(
        Kecamatan,
        on_delete=models.CASCADE
    )

    kode = models.CharField(max_length=20)

    nama = models.CharField(max_length=255)

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

    def __str__(self):
        return f"{self.nama} ({self.kecamatan.nama})"
