from django.db import models
from django.conf import settings
class Dinas(models.Model):
    kode = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=255)

    # kepala = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="dinas_dipimpin"
    # )

    alamat = models.TextField(blank=True)
    telepon = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.nama