
from django.db import models
from core.apps.kelompok.models import Kelompok
from core.apps.legalitas.models import ItemLegalitas
class LegalitasKelompok(models.Model):
    kelompok = models.ForeignKey(Kelompok, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemLegalitas, on_delete=models.CASCADE)

    value = models.TextField()
    
    # Approval status
    aprovalPengawal = models.BooleanField(default=False)
    aprovalDesa = models.BooleanField(default=False)
    aprovalKec = models.BooleanField(default=False)

    # Catatan approval
    ketPengawal = models.TextField(blank=True, null=True)
    ketDesa = models.TextField(blank=True, null=True)
    ketKec = models.TextField(blank=True, null=True)

    # Tanggal approval
    tglPengawal = models.DateField(blank=True, null=True)
    tglDesa = models.DateField(blank=True, null=True)
    tglKec = models.DateField(blank=True, null=True)
