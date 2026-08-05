from django.db import models
from django.conf import settings

from core.apps.master.Bidang.models import Bidang
from core.apps.pengaduan.models import Pengaduan


class PengaduanHistory(models.Model):

    pengaduan = models.ForeignKey(
        Pengaduan,
        on_delete=models.CASCADE,
        related_name="history"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )

    judul = models.CharField(
        max_length=255
    )

    deskripsi = models.TextField()

    status_lama = models.CharField(
        max_length=25
    )

    status_baru = models.CharField(
        max_length=25
    )

    bidang = models.ForeignKey(
        Bidang,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    dokumentasi = models.FileField(
        upload_to="history/",
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )