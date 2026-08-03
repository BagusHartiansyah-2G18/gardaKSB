from django.db import models
from core.apps.organisasi.models import Organisasi
from core.apps.organisasi.PersyaratanOrganisasi.models import PersyaratanOrganisasi
from core.apps.accounts.User.models import User 

class DokumenOrganisasi(models.Model):

    STATUS_CHOICES = (
        ("MENUNGGU", "Menunggu"),
        ("DISETUJUI", "Disetujui"),
        ("DITOLAK", "Ditolak"),
    )

    organisasi = models.ForeignKey(
        Organisasi,
        on_delete=models.CASCADE,
        related_name="dokumen"
    )

    persyaratan = models.ForeignKey(
        PersyaratanOrganisasi,
        on_delete=models.CASCADE
    )

    file = models.FileField(
        upload_to="organisasi/"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="MENUNGGU"
    )

    catatan_verifikasi = models.TextField(
        blank=True
    )

    verified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )