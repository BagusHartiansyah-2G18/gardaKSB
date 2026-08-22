
from django.urls import path

from core.views import (
    save_device_token,send_pending_notifications
)
urlpatterns = [
    path('device-tokens/', save_device_token, name='save-device-token'),
    path( "notifications/send-pending/", send_pending_notifications, name="send-pending-notifications", ),
] 

