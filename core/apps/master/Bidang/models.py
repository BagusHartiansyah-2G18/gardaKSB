from django.db import models
from core.apps.master.Dinas.models import Dinas 
from django.conf import settings

class Bidang(models.Model):
    dinas = models.ForeignKey(
        Dinas,
        on_delete=models.CASCADE
    )

    kode = models.CharField(max_length=20)

    nama = models.CharField(max_length=255)

    # kepala_bidang = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="bidang_dipimpin"
    # )

    deskripsi = models.TextField(blank=True)

    def __str__(self):
        return self.nama