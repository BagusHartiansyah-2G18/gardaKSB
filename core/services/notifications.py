# notifications/services.py
from core.apps.informasi.models import Notifikasi
from core.apps.informasi.DeviceToken.models import DeviceToken
from .firebase import send_push_notification

def process_pending_notifications():
    notifications = Notifikasi.objects.filter(
        status_kirim=False
    ).select_related("user")

    total = notifications.count()
    berhasil = 0
    gagal = 0

    for notification in notifications:

        devices = DeviceToken.objects.filter(
            user=notification.user,
            is_active=True,
            platform="WEB"
        )

        if not devices.exists():
            gagal += 1
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

            except Exception:
                pass

        if notification_sent:
            notification.status_kirim = True
            notification.save(update_fields=["status_kirim"])
            berhasil += 1
        else:
            gagal += 1

    return {
        "total": total,
        "berhasil": berhasil,
        "gagal": gagal,
    }