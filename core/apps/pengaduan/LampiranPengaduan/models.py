from django.db import models
from core.apps.pengaduan.models import Pengaduan 

class LampiranPengaduan(models.Model):
    pengaduan = models.ForeignKey(
        Pengaduan,
        on_delete=models.CASCADE
    )

    file = models.FileField(
        upload_to="pengaduan/"
    )

    jenis_file = models.CharField(
        max_length=50
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )