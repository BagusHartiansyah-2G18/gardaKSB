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


class AnggotaKelompok(models.Model):
    kelompok = models.ForeignKey('Kelompok', on_delete=models.CASCADE)

    nama = models.CharField(max_length=150)
    nik = models.CharField(max_length=20, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    noHp = models.CharField(max_length=20, blank=True, null=True)

    jabatan = models.CharField(
        max_length=50,
        choices=[
            ('ketua', 'Ketua'),
            ('sekretaris', 'Sekretaris'),
            ('bendahara', 'Bendahara'),
            ('anggota', 'Anggota'),
        ],
        default='anggota'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama} ({self.kelompok.nmKelo})"

class AsetKelompok(models.Model):
    kelompok = models.ForeignKey('Kelompok', on_delete=models.CASCADE)

    namaAset = models.CharField(max_length=150)
    kategori = models.CharField(max_length=100, blank=True, null=True)

    jumlah = models.IntegerField(default=1)

    kondisi = models.CharField(
        max_length=20,
        choices=[
            ('baik', 'Baik'),
            ('rusak', 'Rusak'),
            ('perlu_perbaikan', 'Perlu Perbaikan'),
        ],
        default='baik'
    )

    nilai = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    keterangan = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.namaAset} ({self.kelompok.nmKelo})"