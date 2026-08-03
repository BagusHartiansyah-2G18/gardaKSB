from django.db import models

from core.apps.accounts.User.models import User
from core.apps.informasi.MateriBerita.models import MateriBerita


class MateriBeritaActivity(models.Model):

    AKTIVITAS_CHOICES = (
        ("LIKE", "Like"),
        ("VIEW", "View"),
    )

    materi = models.ForeignKey(
        MateriBerita,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    aktivitas = models.CharField(
        max_length=10,
        choices=AKTIVITAS_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):
        if self.kategori == "MATERI" and not self.file_pdf:
            raise ValidationError(
                "File PDF wajib untuk kategori MATERI."
            )
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    class Meta:
        indexes = [
            models.Index(
                fields=["materi", "aktivitas"]
            )
        ]