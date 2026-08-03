from core.apps.pengaduan.models import Pengaduan
from django.db.models import Q,Count 
from django.utils import timezone
 
def getMapKasus():
    return list(
        Pengaduan.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False,
        )
        .select_related(
            "jenis_kasus",
            "desa",
        )
        .values(
            "id",
            "nomor_tiket",
            "nama_pelapor",
            "lokasi_kejadian",
            "latitude",
            "longitude",
            "status",
            "prioritas",
            "desa__nama",
            "jenis_kasus__nama",
            "jenis_kasus__warna",
        )
    ) 

def getGrafikJenisKasus():

    data = list(
        Pengaduan.objects
        .values(
            "jenis_kasus__nama",
            "jenis_kasus__warna"
        )
        .annotate(
            total=Count("id")
        )
        .order_by("-total")
    )

    return {
        "labels": [
            item["jenis_kasus__nama"]
            for item in data
        ],
        "data": [
            item["total"]
            for item in data
        ],
        "colors": [
            item["jenis_kasus__warna"]
            for item in data
        ]
    }

def generateNomorTiket():
    tahun = timezone.now().year

    total = (
        Pengaduan.objects.filter(
            created_at__year=tahun
        ).count() + 1
    )

    return (
        f"GARDA-KSB-{tahun}-"
        f"{str(total).zfill(6)}"
    )