from django.db import models
from core.apps.accounts.User.models import User 
from core.apps.organisasi.JenisOrganisasi.models import JenisOrganisasi 
from core.apps.master.Desa.models import Desa 

class Organisasi(models.Model):

    jenis_organisasi = models.ForeignKey(
        JenisOrganisasi,
        on_delete=models.PROTECT
    )

    nama_organisasi = models.CharField(
        max_length=255
    )

    ketua = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    desa = models.ForeignKey(
        Desa,
        null=True,
        on_delete=models.SET_NULL
    )

    alamat = models.TextField()

    nomor_sk = models.CharField(
        max_length=100,
        blank=True
    )

    tanggal_sk = models.DateField(
        null=True,
        blank=True
    )

    tanggal_berdiri = models.DateField(
        null=True,
        blank=True
    )

    no_hp = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    logo = models.ImageField(
        upload_to="organisasi/",
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    status_verifikasi = models.BooleanField(
        default=False
    )
    def __str__(self):
        return self.nama_organisasi