from django.db import models
from core.apps.wilayah.models import Desa
class Kelompok(models.Model):
    nmKelo = models.CharField(max_length=150)
    desa = models.ForeignKey(Desa, on_delete=models.CASCADE)
    kelas = models.CharField(max_length=50)
    ketua = models.CharField(max_length=100)
    koordinat = models.CharField(max_length=100)