from django.db import models

from core.apps.accounts.User.models import User
from core.apps.master.Desa.models import Desa
from core.apps.master.Bidang.models import Bidang
from core.apps.pengaduan.JenisKasus.models import JenisKasus


class Pengaduan(models.Model):

    STATUS_CHOICES = (
        ("BARU", "Baru"),
        ("VERIFIKASI", "Verifikasi"),
        ("PIMPINAN", "Menunggu Pimpinan"),
        ("PROSES", "Proses"),
        ("MONITORING", "Monitoring"),
        ("SELESAI", "Selesai"),
        ("DITUTUP", "Ditutup"),
        ("DITOLAK", "Ditolak"),
    )

    PRIORITAS_CHOICES = (
        ("RENDAH", "Rendah"),
        ("SEDANG", "Sedang"),
        ("TINGGI", "Tinggi"),
        ("DARURAT", "Darurat"),
    )

    SOURCE_CHOICES = (
        ("WEB", "Web"),
        ("ANDROID", "Android"),
        ("IOS", "iOS"),
        ("ADMIN", "Admin"),
    )

    nomor_tiket = models.CharField(
        max_length=50,
        unique=True
    )

    pelapor = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pengaduan"
    )

    nama_pelapor = models.CharField(
        max_length=255
    )

    hp_pelapor = models.CharField(
        max_length=20
    )

    email_pelapor = models.CharField(
        blank=True
    )

    alamat_pelapor = models.TextField(
        blank=True
    )

    anonim = models.BooleanField(
        default=False
    )

    desa = models.ForeignKey(
        Desa,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    jenis_kasus = models.ForeignKey(
        JenisKasus,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    lokasi_kejadian = models.TextField()

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )
    lampiran = models.FileField(
        upload_to="pengaduan/",
        blank=True,
        null=True
    )
    waktu_kejadian = models.DateTimeField()
    judul = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )
    uraian = models.TextField()

    pihak_terlibat = models.TextField(
        blank=True
    )

    dampak = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="BARU"
    )

    prioritas = models.CharField(
        max_length=20,
        choices=PRIORITAS_CHOICES,
        default="SEDANG"
    )

    bidang_disposisi = models.ForeignKey(
        Bidang,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    verifikator = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pengaduan_verifikasi"
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )

    disposisi_oleh = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pengaduan_disposisi"
    )

    disposisi_at = models.DateTimeField(
        null=True,
        blank=True
    )

    petugas = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pengaduan_penanganan"
    )

    verifikasi_admin = models.BooleanField(
        default=False
    )

    tindak_lanjut = models.TextField(
        blank=True
    )

    kesimpulan = models.TextField(
        blank=True
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default="WEB"
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pengaduan"
        verbose_name_plural = "Pengaduan"

    def __str__(self):
        return f"{self.nomor_tiket} - {self.nama_pelapor}"