from django.db import models
from core.apps.usaha.models import ListUsaha

class Pendapatan(models.Model):
    
    JENIS_CHOICES = (
        ('UMUM', 'Umum'),
        ('PADES', 'PADes'),
        ('PAJAK', 'Pajak'),
    )

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
    jenis = models.CharField(
        max_length=10,
        choices=JENIS_CHOICES,
        default='UMUM'
    )

    def __str__(self):
        return f"{self.usaha} - {self.dateCreate}"
    
    
    def save(self, *args, **kwargs):
        self.laba = self.pendapatan - self.pengeluaran
        

        qs = Pendapatan.objects.filter(
            usaha=self.usaha
        )

        if self.pk:
            qs = qs.exclude(pk=self.pk)

        last = qs.order_by('-dateCreate', '-id').first()

        if last:
            self.kas = last.kas + self.laba
        else:
            self.kas = self.laba

        super().save(*args, **kwargs)

