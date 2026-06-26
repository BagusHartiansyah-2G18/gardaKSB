from django.db import models
from django.contrib.auth.models import User

class Kecamatan(models.Model):
    nmKec = models.CharField(max_length=100)

class Desa(models.Model):
    nmDesa = models.CharField(max_length=100)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
 
class WilayahPengawas(models.Model):
    
    desa = models.ForeignKey(Desa, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user} - {self.desa}"
