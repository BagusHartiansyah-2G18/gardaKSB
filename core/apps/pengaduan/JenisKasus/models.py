from django.db import models
class JenisKasus(models.Model):

    kode = models.CharField(
        max_length=20
    )

    nama = models.CharField(
        max_length=255
    )
    
    warna = models.CharField(
        max_length=7,
        default="#facc15",
        help_text="Format HEX, contoh #ef4444"
    )
    def __str__(self):
        return self.nama