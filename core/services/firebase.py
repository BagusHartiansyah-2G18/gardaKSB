 
import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings


if not firebase_admin._apps:
    cred = credentials.Certificate(
        settings.FIREBASE_SERVICE_ACCOUNT
    )

    firebase_admin.initialize_app(cred)


def send_push_notification(
    token,
    title,
    body,
    url="",
    jenis="SISTEM",
):
    # print(f"Sending push notification to token: {token}")
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data={
            "url": url,
            "jenis": jenis,
        },
        token=token,
    )

    return messaging.send(message) 