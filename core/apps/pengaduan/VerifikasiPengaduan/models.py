from django.db import models
from core.apps.pengaduan.models import Pengaduan 
from django.conf import settings

class VerifikasiPengaduan(models.Model):

    ROLE = (
        ("PJ","Penanggung Jawab"),
        ("TIM","Tim / Anggota"),
    )

    pengaduan = models.ForeignKey(
        Pengaduan,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    peran = models.CharField(
        max_length=10,
        choices=ROLE
    )

    status_verifikasi = models.BooleanField(
        default=False
    )

    catatan = models.TextField(
        blank=True
    )

    tanggal_verifikasi = models.DateTimeField(
        null=True,
        blank=True
    )