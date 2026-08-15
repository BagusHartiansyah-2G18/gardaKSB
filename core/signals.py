import logging

from threading import Thread
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.pengaduan.models import Pengaduan
from core.apps.accounts.User.models import User
from core.apps.informasi.models import Notifikasi
from core.services.notifications import (
    process_pending_notifications
)

logger = logging.getLogger(__name__)


def safe_process_notifications():

    try:

        process_pending_notifications()

    except Exception:

        logger.exception(
            "Gagal memproses notifikasi"
        )


@receiver(post_save, sender=Pengaduan)
def buat_notifikasi_pengaduan(
    sender,
    instance,
    created,
    **kwargs
):

    if not created:
        return

    admins = User.objects.filter(
        groups__name__in=[
            "ADMIN",
            "KABAN",
            "INTEL",
            "SEKBAN",
        ]
    ).distinct()

    for admin in admins:

        try:

            Notifikasi.objects.create(
                user=admin,
                judul=instance.judul,
                pesan=instance.uraian,
                url=(
                    f"https://garda.kabsumbawabarat.com/"
                    f"admin/pengaduan/pengaduan/"
                    f"{instance.id}/change/"
                )
            )

        except Exception:

            logger.exception(
                "Gagal membuat notifikasi"
            )


@receiver(post_save, sender=Notifikasi)
def kirim_notifikasi_otomatis(
    sender,
    instance,
    created,
    **kwargs
):

    if not created:
        return

    transaction.on_commit(
        lambda: Thread(
            target=safe_process_notifications,
            daemon=True
        ).start()
    )
    
# from django.db.models.signals import post_delete, post_save
# from django.dispatch import receiver 
# from core.apps.pengaduan.models import Pengaduan 
# from core.services.notifications import process_pending_notifications
# from core.apps.accounts.User.models import User
# from core.apps.informasi.models import Notifikasi
# from django.db import transaction
# from threading import Thread


# @receiver(post_save, sender=Pengaduan)
# def buat_notifikasi_pengaduan(sender, instance, created, **kwargs):
#     if created:
#         # admins = User.objects.filter(is_superuser=True)
#         admins = User.objects.filter(
#             groups__name__in=[
#                 "ADMIN",
#                 "KABAN",
#                 "INTEL",
#                 "SEKBAN",
#             ]
#         ).distinct()

#         for admin in admins:
#             Notifikasi.objects.create(
#                 user=admin,
#                 judul=instance.judul,
#                 pesan=instance.uraian,
#                 url=f"https://garda.kabsumbawabarat.com/admin/pengaduan/pengaduan/{instance.id}/change/"
#             ) 
#     transaction.on_commit(
#         lambda: Thread(
#             target=process_pending_notifications,
#             daemon=True
#         ).start()
#     ) 

# @receiver(post_save, sender=Notifikasi)
# def kirim_notifikasi_otomatis(
#     sender,
#     instance,
#     created,
#     **kwargs
# ):
#     if not created:
#         return

#     transaction.on_commit(
#         lambda: process_pending_notifications()
#     )