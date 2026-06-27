from django.db import models
from core.apps.wilayah.models import Desa
from core.apps.legalitas.models import ItemLegalitas

class Kelompok(models.Model):
    nmKelo = models.CharField(max_length=150)
    desa = models.ForeignKey(Desa, on_delete=models.CASCADE)
    kelas = models.CharField(max_length=50)
    ketua = models.CharField(max_length=100)
    koordinat = models.CharField(max_length=100)
    def __str__(self):
        return self.nmKelo


class LegalitasKelompok(models.Model):
    kelompok = models.ForeignKey(Kelompok, on_delete=models.CASCADE)
    itemLegalitas = models.ForeignKey(ItemLegalitas, on_delete=models.CASCADE)

    value = models.CharField(max_length=255, blank=True, null=True)

    # ✅ APPROVAL STATUS
    aprovalPengawal = models.BooleanField(default=False)
    aprovalDesa = models.BooleanField(default=False)
    aprovalKec = models.BooleanField(default=False)

    # ✅ CATATAN
    ketPengawal = models.TextField(blank=True, null=True)
    ketDesa = models.TextField(blank=True, null=True)
    ketKec = models.TextField(blank=True, null=True)

    # ✅ TANGGAL APPROVAL
    tglPengawal = models.DateField(blank=True, null=True)
    tglDesa = models.DateField(blank=True, null=True)
    tglKec = models.DateField(blank=True, null=True)

    # ✅ metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('kelompok', 'itemLegalitas')

    def __str__(self):
        return f"{self.kelompok} - {self.itemLegalitas}"

