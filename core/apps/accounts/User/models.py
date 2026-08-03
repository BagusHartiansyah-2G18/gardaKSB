from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("KABAN", "Kaban"),
        ("SEKBAN", "Sekban"),
        ("KABID", "Kabid"),
        ("ANGGOTA", "Anggota"),
        ("MASYARAKAT", "Masyarakat"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="MASYARAKAT"
    )

    nik = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )

    no_hp = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.get_full_name() or self.username