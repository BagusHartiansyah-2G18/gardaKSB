from django.db import models
class Kecamatan(models.Model):
    kode = models.CharField(max_length=20)

    nama = models.CharField(max_length=255)

    def __str__(self):
        return self.nama 