from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver 
from core.apps.pengaduan.models import Pengaduan 
from core.services.notifications import process_pending_notifications
from core.apps.accounts.User.models import User
from core.apps.informasi.models import Notifikasi

@receiver(post_save, sender=Pengaduan)
def buat_notifikasi_pengaduan(sender, instance, created, **kwargs):
    if created:
        # admins = User.objects.filter(is_superuser=True)
        admins = User.objects.filter(
            groups__name__in=[
                "ADMIN",
                "KABAN",
                "INTEL",
                "SEKBAN",
            ]
        ).distinct()

        for admin in admins:
            Notifikasi.objects.create(
                user=admin,
                judul=instance.judul,
                pesan=instance.uraian,
                url=f"/pengaduan/{instance.id}/"
            ) 

@receiver(post_save, sender=Notifikasi)
def kirim_notifikasi_otomatis(sender, instance, created, **kwargs):
    if created:
        process_pending_notifications()