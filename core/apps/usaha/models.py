from django.db import models
from core.apps.kelompok.models import Kelompok
class JenisUsaha(models.Model):
    nmJUsaha = models.CharField(max_length=100)


class ListUsaha(models.Model):
    kelompok = models.ForeignKey(Kelompok, on_delete=models.CASCADE)
    jenisUsaha = models.ForeignKey(JenisUsaha, on_delete=models.CASCADE)
    komoditi = models.CharField(max_length=100)
    wadah = models.CharField(max_length=100)
    teknologi = models.CharField(max_length=100)
    lahan = models.CharField(max_length=100)
    tglMulai = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
