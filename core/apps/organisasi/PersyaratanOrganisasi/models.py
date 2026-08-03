from django.db import models
from core.apps.organisasi.JenisOrganisasi.models import JenisOrganisasi

class PersyaratanOrganisasi(models.Model):

    jenis_organisasi = models.ForeignKey(
        JenisOrganisasi,
        on_delete=models.CASCADE
    )

    nama = models.CharField(max_length=255)

    wajib = models.BooleanField(default=True)

    def __str__(self):
        return self.nama