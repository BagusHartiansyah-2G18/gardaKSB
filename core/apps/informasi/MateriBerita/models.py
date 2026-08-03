from django.db import models
from core.apps.accounts.User.models import User 

class MateriBerita(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    kategori = models.CharField(
        max_length=20,
        choices=(
            ("BERITA", "Berita"),
            ("MATERI", "Materi"),
        )
    )

    judul = models.CharField(
        max_length=255
    )

    slug = models.SlugField(
        unique=True
    )

    deskripsi = models.TextField()

    cover_image = models.ImageField(
        upload_to="materi/"
    )
    file_pdf = models.FileField(
        upload_to="materi/pdf/",
        null=True,
        blank=True
    )

    is_public = models.BooleanField(
        default=False
    )

    status_publish = models.BooleanField(
        default=False
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True
    )