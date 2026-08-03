from core.apps.informasi.MateriBerita.models import MateriBerita


def getRandom_berita(limit=5, kategori="BERITA",is_public=True,status_publish=True):
    """
    Ambil berita publik yang sudah publish secara random.
    """
    return (
        MateriBerita.objects.filter(
            kategori=kategori,
            is_public=is_public,
            status_publish=status_publish,
        )
        .order_by("?")[:limit]
    )