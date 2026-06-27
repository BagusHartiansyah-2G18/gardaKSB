from django.db import models
from core.apps.kelompok.models import Kelompok
class JenisUsaha(models.Model):
    nmJUsaha = models.CharField(max_length=100)
    def __str__(self):
        return self.nmJUsaha

class ListUsaha(models.Model):
    kelompok = models.ForeignKey(Kelompok, on_delete=models.CASCADE)
    jenisUsaha = models.ForeignKey(JenisUsaha, on_delete=models.CASCADE)
    komoditi = models.CharField(max_length=100)
    wadah = models.CharField(max_length=100)
    teknologi = models.CharField(max_length=100)
    lahan = models.CharField(max_length=100)
    tglMulai = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.jenisUsaha.nmJUsaha} - {self.komoditi}"

   
