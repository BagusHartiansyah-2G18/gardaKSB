from django.db import models
from core.apps.usaha.models import ListUsaha

class Pendapatan(models.Model):
    usaha = models.ForeignKey(ListUsaha, on_delete=models.CASCADE)
    dateCreate = models.DateField()

    pendapatan = models.FloatField()
    pengeluaran = models.FloatField()
    laba = models.FloatField()
    kas = models.FloatField()

    keterangan = models.TextField(blank=True, null=True)

    # Approval status
    aprovalPengawal = models.BooleanField(default=False)
    aprovalDesa = models.BooleanField(default=False)
    aprovalKec = models.BooleanField(default=False)

    # Catatan approval
    ketPengawal = models.TextField(blank=True, null=True)
    ketDesa = models.TextField(blank=True, null=True)
    ketKec = models.TextField(blank=True, null=True)

    # Tanggal approval
    tglPengawal = models.DateField(blank=True, null=True)
    tglDesa = models.DateField(blank=True, null=True)
    tglKec = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.usaha} - {self.dateCreate}"
    
    
    def save(self, *args, **kwargs):

        # ✅ hitung laba otomatis
        self.laba = self.pendapatan - self.pengeluaran

        # ✅ ambil kas terakhir dari usaha yang sama
        last = Pendapatan.objects.filter(
            usaha=self.usaha
        ).order_by('-dateCreate', '-id').first()

        if last:
            self.kas = last.kas + self.laba
        else:
            self.kas = self.laba  # awal

        super().save(*args, **kwargs)
