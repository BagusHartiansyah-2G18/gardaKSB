from django.db import models
from core.apps.accounts.User.models import User


class Notifikasi(models.Model):

    JENIS_CHOICES = (
        ("PENGADUAN", "Pengaduan"),
        ("ORGANISASI", "Organisasi"),
        ("BERITA", "Berita"),
        ("SISTEM", "Sistem"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    jenis = models.CharField(
        max_length=20,
        choices=JENIS_CHOICES,
        default="SISTEM"
    )

    judul = models.CharField(
        max_length=255
    )

    pesan = models.TextField()

    url = models.CharField(
        max_length=255,
        blank=True
    )

    status_baca = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.judul