# notifications/services.py

import logging

from core.apps.informasi.models import (
    Notifikasi
)
from core.apps.informasi.DeviceToken.models import (
    DeviceToken
)
from .firebase import (
    send_push_notification
)
from firebase_admin._messaging_utils import (
    UnregisteredError
)

logger = logging.getLogger(__name__)


def process_pending_notifications():

    notifications = (
        Notifikasi.objects
        .filter(
            status_kirim=False
        )
        .select_related(
            "user"
        )
    )

    total = notifications.count()
    print(f"pending : {total}")
    berhasil = 0
    gagal = 0

    for notification in notifications:

        try:

            devices = (
                DeviceToken.objects
                .filter(
                    user=notification.user,
                    is_active=True,
                )
            )

            if not devices.exists():

                gagal += 1

                logger.warning(
                    (
                        "Tidak ada device token "
                        "untuk user %s"
                    ),
                    notification.user_id,
                )

                continue

            notification_sent = False

            for device in devices:

                try:

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
                        "Token tidak valid, hapus: %s",
                        device.token
                    )

                    device.delete()

                except Exception:

                    logger.exception(
                        (
                            "Gagal kirim push "
                            "notification "
                            "ke token %s"
                        ),
                        device.token,
                    )

            if notification_sent:

                notification.status_kirim = True

                notification.save(
                    update_fields=[
                        "status_kirim"
                    ]
                )

                berhasil += 1

            else:

                gagal += 1

        except Exception:

            gagal += 1

            logger.exception(
                (
                    "Error saat memproses "
                    "notifikasi %s"
                ),
                notification.id,
            )

    logger.info(
        (
            "Notifikasi selesai "
            "diproses. "
            "Total=%s "
            "Berhasil=%s "
            "Gagal=%s"
        ),
        total,
        berhasil,
        gagal,
    )

    return {
        "total": total,
        "berhasil": berhasil,
        "gagal": gagal,
    }
# # notifications/services.py
# from core.apps.informasi.models import Notifikasi
# from core.apps.informasi.DeviceToken.models import DeviceToken
# from .firebase import send_push_notification

# def process_pending_notifications():
#     notifications = Notifikasi.objects.filter(
#         status_kirim=False
#     ).select_related("user")

#     total = notifications.count()
#     berhasil = 0
#     gagal = 0

#     for notification in notifications:

#         devices = DeviceToken.objects.filter(
#             user=notification.user,
#             is_active=True,
#             platform="WEB"
#         )

#         if not devices.exists():
#             gagal += 1
#             continue

#         notification_sent = False

#         for device in devices:
#             try:
#                 send_push_notification(
#                     token=device.token,
#                     title=notification.judul,
#                     body=notification.pesan,
#                     url=notification.url,
#                     jenis=notification.jenis,
#                 )

#                 notification_sent = True

#             except Exception:
#                 pass

#         if notification_sent:
#             notification.status_kirim = True
#             notification.save(update_fields=["status_kirim"])
#             berhasil += 1
#         else:
#             gagal += 1

#     return {
#         "total": total,
#         "berhasil": berhasil,
#         "gagal": gagal,
#     }