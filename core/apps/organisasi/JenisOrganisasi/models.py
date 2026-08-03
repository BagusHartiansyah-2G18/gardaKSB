from django.db import models 
class JenisOrganisasi(models.Model):

    kode = models.CharField(
        max_length=20,
        unique=True
    )

    nama = models.CharField(
        max_length=255
    )

    deskripsi = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Jenis Organisasi"
        verbose_name_plural = "Jenis Organisasi"
        ordering = ["nama"]

    def __str__(self):
        return self.nama