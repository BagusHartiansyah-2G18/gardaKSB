from django.db import models
from core.apps.master.models import Kecamatan 

class Desa(models.Model):
    kecamatan = models.ForeignKey(
        Kecamatan,
        on_delete=models.CASCADE
    )

    kode = models.CharField(max_length=20)

    nama = models.CharField(max_length=255)

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.nama} ({self.kecamatan.nama})"
