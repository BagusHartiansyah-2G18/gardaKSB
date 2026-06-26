from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # role user
    ROLE_CHOICES = [
        ('kelompok', 'Kelompok'),
        ('pengawal', 'Pengawal'),
        ('desa', 'Desa'),
        ('kecamatan', 'Kecamatan'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # relasi wilayah (bisa fleksibel)
    idWilayah = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
