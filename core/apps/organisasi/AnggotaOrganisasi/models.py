from django.db import models
from core.apps.organisasi.models import Organisasi 

class AnggotaOrganisasi(models.Model):
    organisasi = models.ForeignKey(
        Organisasi,
        on_delete=models.CASCADE
    )

    nama = models.CharField(max_length=255)
    nik = models.CharField(max_length=16)
    jabatan = models.CharField(max_length=100)

    no_hp = models.CharField(
        max_length=20,
        blank=True
    )

    alamat = models.TextField(
        blank=True
    )