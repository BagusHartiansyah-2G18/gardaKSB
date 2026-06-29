
from core.apps.wilayah.models import WilayahPengawas

def getWilaya(request):
    user = request.user

    if user.is_superuser:
        return None  # ✅ artinya semua akses

    return WilayahPengawas.objects.filter(
        user=user
    ).values_list('desa_id', flat=True).distinct()


def isakses(request):
    user = request.user
    if user.is_superuser:
        return None
    elif user.is_staff:
        return True
    return False
        