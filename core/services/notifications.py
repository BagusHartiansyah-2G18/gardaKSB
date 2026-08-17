import logging
import time

from firebase_admin._messaging_utils import (
    UnregisteredError
)

from core.apps.informasi.models import (
    Notifikasi
)

from core.apps.informasi.DeviceToken.models import (
    DeviceToken
)

from .firebase import (
    send_push_notification
)

logger = logging.getLogger(__name__)


def process_pending_notifications():

    start_time = time.time()

    notifications = list(
        Notifikasi.objects
        .filter(
            status_kirim=False
        )
        .select_related(
            "user"
        )
    )

    total = len(notifications)

    logger.info(
        "Pending notifications: %s",
        total
    )

    berhasil = 0
    gagal = 0

    for notification in notifications:

        try:

            logger.info(
                "Memproses notifikasi id=%s user=%s",
                notification.id,
                notification.user_id,
            )

            devices = list(
                DeviceToken.objects
                .filter(
                    user=notification.user,
                    is_active=True,
                )
            )

            if not devices:

                gagal += 1

                logger.warning(
                    "Tidak ada device token untuk user %s",
                    notification.user_id,
                )

                continue

            notification_sent = False

            for device in devices:

                try:

                    logger.info(
                        "Kirim ke token=%s",
                        device.token[:20]
                    )

                    send_push_notification(
                        token=device.token,
                        title=notification.judul,
                        body=notification.pesan,
                        url=notification.url,
                        jenis=notification.jenis,
                    )

                    notification_sent = True

                except UnregisteredError:

                    logger.warning(
                        "Token tidak valid. Hapus token=%s",
                        device.token[:20]
                    )

                    device.delete()

                except Exception:

                    logger.exception(
                        "Gagal kirim push notification ke token=%s",
                        device.token[:20]
                    )

            if notification_sent:

                notification.status_kirim = True

                notification.save(
                    update_fields=[
                        "status_kirim"
                    ]
                )

                berhasil += 1

                logger.info(
                    "Notifikasi id=%s berhasil dikirim",
                    notification.id
                )

            else:

                gagal += 1

                logger.warning(
                    "Notifikasi id=%s gagal terkirim",
                    notification.id
                )

        except Exception:

            gagal += 1

            logger.exception(
                "Error saat memproses notifikasi id=%s",
                notification.id,
            )

    duration = time.time() - start_time

    logger.info(
        (
            "Process notification selesai. "
            "Total=%s Berhasil=%s Gagal=%s "
            "Durasi=%.2f detik"
        ),
        total,
        berhasil,
        gagal,
        duration,
    )

    return {
        "total": total,
        "berhasil": berhasil,
        "gagal": gagal,
    }