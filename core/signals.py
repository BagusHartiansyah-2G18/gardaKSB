import logging
import time

from threading import Lock, Thread

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

notification_lock = Lock()

last_notification_time = 0
DEBOUNCE_SECONDS = 5


def safe_process_notifications():

    global last_notification_time

    current_time = time.time()
    last_notification_time = current_time

    logger.info(
        "Notifikasi diterima, menunggu %s detik.",
        DEBOUNCE_SECONDS
    )

    time.sleep(DEBOUNCE_SECONDS)

    if last_notification_time != current_time:

        logger.info(
            "Ada notifikasi baru masuk. Batalkan batch lama."
        )

        return

    if not notification_lock.acquire(
        blocking=False
    ):

        logger.info(
            "Process notification sedang berjalan. Skip."
        )

        return

    try:

        logger.info(
            "Mulai process_pending_notifications."
        )

        result = process_pending_notifications()

        logger.info(
            (
                "Selesai process_pending_notifications. "
                "Total=%s Berhasil=%s Gagal=%s"
            ),
            result.get("total", 0),
            result.get("berhasil", 0),
            result.get("gagal", 0),
        )

    except Exception:

        logger.exception(
            "Gagal memproses notifikasi."
        )

    finally:

        notification_lock.release()

        logger.info(
            "Notification lock released."
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
                    "https://garda.kabsumbawabarat.com/"
                    f"admin/pengaduan/pengaduan/"
                    f"{instance.id}/change/"
                )
            )

        except Exception:

            logger.exception(
                "Gagal membuat notifikasi untuk user=%s",
                admin.id
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