from core.apps.informasi.MateriBerita.models import MateriBerita
from core.apps.informasi.MateriBeritaActivity.models import MateriBeritaActivity
from django.db.models import Count, Exists, OuterRef
from core.apps.accounts.User.models import User 

from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from core.apps.informasi.MateriBerita.models import MateriBerita


from django.db.models import Count

from django.db.models import Count, Q
def getBeritaON( 
    kategori="MATERI",
    is_public=True,
    status_publish=True,
):
    return (
        MateriBerita.objects.filter(
            kategori=kategori,
            is_public=is_public,
            status_publish=status_publish,
        )
        .annotate(
            total_like=Count(
                "activities",
                filter=Q(
                    activities__aktivitas="LIKE"
                )
            ),
            total_view=Count(
                "activities",
                filter=Q(
                    activities__aktivitas="VIEW"
                )
            ),
        )
        .values(
            "id",
            "judul",
            "deskripsi",
            "slug",
            "cover_image",
            "published_at",
            "file_pdf",
            "total_like",
            "total_view",
            "user__username",
        )
        .order_by("?")
    )

def getDetailBerita(slug):
    return get_object_or_404(
        MateriBerita.objects.annotate(
            total_like=Count(
                "activities",
                filter=Q(
                    activities__aktivitas="LIKE"
                )
            ),
            total_view=Count(
                "activities",
                filter=Q(
                    activities__aktivitas="VIEW"
                )
            ),
        ),
        slug=slug
    )
def getRandom_berita(
    limit=5,
    kategori="MATERI",
    is_public=True,
    status_publish=True,
):
    return (
        MateriBerita.objects.filter(
            kategori=kategori,
            is_public=is_public,
            status_publish=status_publish,
        )
        .annotate(
            total_like=Count(
                "activities",
                filter=Q(
                    activities__aktivitas="LIKE"
                )
            ),
            total_view=Count(
                "activities",
                filter=Q(
                    activities__aktivitas="VIEW"
                )
            ),
        )
        .values(
            "id",
            "judul",
            "deskripsi",
            "slug",
            "cover_image",
            "published_at",
            "total_like",
            "total_view",
            "user__username",
        )
        .order_by("?")[:limit]
    )
def toggle_like(user, materi_id):

    materi = MateriBerita.objects.get(
        id=materi_id
    )

    like = MateriBeritaActivity.objects.filter(
        user=user,
        materi=materi,
        aktivitas="LIKE"
    )

    if like.exists():
        like.delete()
        return False

    MateriBeritaActivity.objects.create(
        user=user,
        materi=materi,
        aktivitas="LIKE"
    )

    return True 
 
from django.db.models import Q, Count

from core.apps.informasi.MateriBerita.models import (
    MateriBerita
)


def getFileMateriPerBidang(
    bidang_id=None,
    kategori="MATERI",
    is_public=True,
    id=None,
    status_publish=True,
):

    qs = (
        MateriBerita.objects
        .filter(
            kategori=kategori,
            is_public=is_public,
            status_publish=status_publish,
            file_pdf__isnull=False,
        )
    )

    if bidang_id:
        
        qs = qs.filter(
            user__userprofile__bidang_id=bidang_id
        ) 
    if id:
        qs = qs.filter(
            id=id
        )
         
    return (
        qs

        .annotate(

            total_like=Count(
                "activities",
                filter=Q(
                    activities__aktivitas="LIKE"
                )
            ),

            total_view=Count(
                "activities",
                filter=Q(
                    activities__aktivitas="VIEW"
                )
            ),

        )

        .values(
            "id",
            "judul",
            "deskripsi",
            "slug",
            "cover_image",
            "published_at",
            "total_like",
            "file_pdf",
            "total_view",
            "user__username",
            "user__userprofile__bidang__nama",
        )

        .order_by("-published_at")

    )
def getBeritaPerBulan(kategori="MATERI"):

    data = list(
        MateriBerita.objects.filter(
            kategori=kategori,
            is_public=True,
            status_publish=True,
        )
        .annotate(
            bulan=ExtractMonth("published_at")
        )
        .values("bulan")
        .annotate(
            total=Count("id")
        )
        .order_by("bulan")
    )

    return {
        "total": sum(item["total"] for item in data),
        "labels": [
            item["bulan"]
            for item in data
        ],
        "data": [
            item["total"]
            for item in data
        ]
    }
    
def getMateriPerBidang(kategori="MATERI"):

    data = list(
        MateriBerita.objects.filter(
            kategori=kategori,
            is_public=True,
            status_publish=True,
        )
        .values(
            "user__userprofile__bidang__nama"
        )
        .annotate(
            total=Count("id")
        )
        .order_by("-total")
    )

    return {
        "total": sum(item["total"] for item in data),
        "labels": [
            item["user__userprofile__bidang__nama"] or "-"
            for item in data
        ],
        "data": [
            item["total"]
            for item in data
        ]
    }

def getPartisipasiMateri(kategori="MATERI"):

    total_user = User.objects.count()

    total_uploader = (
        MateriBerita.objects.filter(
            kategori=kategori,
            is_public=True,
            status_publish=True,
        )
        .values("user")
        .distinct()
        .count()
    )

    persentase = 0

    if total_user > 0:
        persentase = round(
            (total_uploader / total_user) * 100,
            2
        )

    return {
        "total_user": total_user,
        "total_uploader": total_uploader,
        "persentase": persentase,
    }