from django.db import models

class ItemLegalitas(models.Model):
    nmILega = models.CharField(max_length=100)
    jenisValue = models.CharField(max_length=20)
    idJLega = models.CharField(max_length=100)