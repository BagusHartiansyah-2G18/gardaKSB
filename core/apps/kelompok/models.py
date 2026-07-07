from django.db import models
from core.apps.wilayah.models import Desa
from core.apps.legalitas.models import ItemLegalitas
from django.contrib.auth.models import User


class Kelompok(models.Model):

    JENIS_KELOMPOK = (
        ('POKTAN', 'POKTAN'),
        ('GAPOKTAN', 'GAPOKTAN'),
        ('BUMDES', 'BUMDES'),
        ('PKK', 'PKK'),
        ('KARANG_TARUNA', 'KARANG TARUNA'),
        ('KDMP', 'KDMP'),
    )

    jenisKelompok = models.CharField(
        max_length=30,
        choices=JENIS_KELOMPOK,
        default='POKTAN'
    )

    desa = models.ForeignKey(
        Desa,
        on_delete=models.CASCADE
    )

    nmKelo = models.CharField(max_length=150)

    kelas = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    ketua = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    jumlahAnggota = models.PositiveIntegerField(
        default=0
    )

    koordinat = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    luasLahan = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
    )

    komoditasUtama = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    statusOperasional = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    tahunBerdiri = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    namaAwal = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    alamat = models.TextField(
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    noHp = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    jumlahPengelola = models.PositiveIntegerField(
        default=0,
        null=True
    )

   
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )


    def __str__(self):
        return f"{self.nmKelo} - {self.desa.nmDesa}"




class LegalitasKelompok(models.Model):

    kelompok = models.ForeignKey(
        Kelompok,
        on_delete=models.CASCADE
    )

    itemLegalitas = models.ForeignKey(
        ItemLegalitas,
        on_delete=models.CASCADE
    )

    value = models.TextField(
        blank=True,
        null=True
    )

    fileDokumen = models.FileField(
        upload_to='legalitas/',
        blank=True,
        null=True
    )

    aprovalPengawal = models.BooleanField(
        default=False
    )

    aprovalDesa = models.BooleanField(
        default=False
    )

    aprovalKec = models.BooleanField(
        default=False
    )

    ketPengawal = models.TextField(
        blank=True,
        null=True
    )

    ketDesa = models.TextField(
        blank=True,
        null=True
    )

    ketKec = models.TextField(
        blank=True,
        null=True
    )

    tglPengawal = models.DateField(
        blank=True,
        null=True
    )

    tglDesa = models.DateField(
        blank=True,
        null=True
    )

    tglKec = models.DateField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'kelompok',
            'itemLegalitas'
        )

    def __str__(self):
        return f"{self.kelompok} - {self.itemLegalitas}"



class AnggotaKelompok(models.Model):

    kelompok = models.ForeignKey(
        Kelompok,
        on_delete=models.CASCADE
    )

    nama = models.CharField(max_length=150)

    nik = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    alamat = models.TextField(
        blank=True,
        null=True
    )

    noHp = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    jabatan = models.CharField(
        max_length=50,
        choices=[
            ('direktur', 'Direktur'),
            ('ketua', 'Ketua'),
            ('sekretaris', 'Sekretaris'),
            ('bendahara', 'Bendahara'),
            ('anggota', 'Anggota'),
        ],
        default='anggota'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nama



class AsetKelompok(models.Model):

    kelompok = models.ForeignKey(
        Kelompok,
        on_delete=models.CASCADE
    )

    namaAset = models.CharField(
        max_length=150
    )

    kategori = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    jumlah = models.IntegerField(
        default=1
    )

    kondisi = models.CharField(
        max_length=20,
        choices=[
            ('baik', 'Baik'),
            ('rusak', 'Rusak'),
            ('perlu_perbaikan', 'Perlu Perbaikan'),
        ],
        default='baik'
    )

    nilai = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
    )

    keterangan = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.namaAset


from smart_selects.db_fields import ChainedForeignKey

class WilayahPengawas(models.Model):

    desa = models.ForeignKey(
        Desa,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    kelompok = ChainedForeignKey(
        Kelompok,
        chained_field="desa",
        chained_model_field="desa",
        show_all=False,
        auto_choose=False,
        sort=True,
        on_delete=models.CASCADE,
        
        null=True,
        blank=True

    )

    def __str__(self):
        return f"{self.user} - {self.desa}"