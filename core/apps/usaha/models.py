from django.db import models
from core.apps.kelompok.models import Kelompok
class JenisUsaha(models.Model):
    nmJUsaha = models.CharField(max_length=100)
    def __str__(self):
        return self.nmJUsaha


class ListUsaha(models.Model):

    kelompok = models.ForeignKey(
        Kelompok,
        on_delete=models.CASCADE
    )

    jenisUsaha = models.ForeignKey(
        JenisUsaha,
        on_delete=models.CASCADE
    )

    # komoditi = models.CharField(
    #     max_length=150
    # )

    # wadah = models.CharField(
    #     max_length=150,
    #     blank=True,
    #     null=True
    # )

    # teknologi = models.CharField(
    #     max_length=150,
    #     blank=True,
    #     null=True
    # )

    # lahan = models.DecimalField(
    #     max_digits=15,
    #     decimal_places=2,
    #     blank=True,
    #     null=True
    # )

    # tglMulai = models.DateField(
    #     null=True,
    #     blank=True
    # )

    # status = models.CharField(
    #     max_length=50,
    #     blank=True,
    #     null=True
    # )

    # penanggungJawab = models.CharField(
    #     max_length=150,
    #     blank=True,
    #     null=True
    # )

    def __str__(self):
        return f"{self.jenisUsaha.nmJUsaha}"


   
