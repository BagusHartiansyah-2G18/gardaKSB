import logging

import firebase_admin

from firebase_admin import (
    credentials,
    messaging
)

from django.conf import settings

logger = logging.getLogger(__name__)

if not firebase_admin._apps:

    cred = credentials.Certificate(
        settings.FIREBASE_SERVICE_ACCOUNT
    )

    firebase_admin.initialize_app(
        cred
    )

    logger.info(
        "Firebase initialized."
    )


def send_push_notification(
    token,
    title,
    body,
    url="",
    jenis="SISTEM",
):

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data={
            "url": url or "",
            "jenis": jenis or "SISTEM",
        },
        token=token,
    )

    logger.info(
        "Mengirim push notification token=%s",
        token[:20]
    )

    response = messaging.send(
        message
    )

    logger.info(
        "Push notification berhasil. message_id=%s",
        response
    )

    return response