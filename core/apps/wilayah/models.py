from django.db import models
from django.contrib.auth.models import User

class Kecamatan(models.Model):
    nmKec = models.CharField(max_length=100) 
    def __str__(self):
        return self.nmKec

class Desa(models.Model):
    nmDesa = models.CharField(max_length=100)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    def __str__(self):
        return self.nmDesa
    
 
class WilayahPengawas(models.Model):
    
    desa = models.ForeignKey(Desa, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.user} - {self.desa}"
