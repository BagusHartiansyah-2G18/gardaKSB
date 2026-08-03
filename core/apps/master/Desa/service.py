from core.apps.master.Desa.models import Desa
def getDesa(search=None):
    qs = (
        Desa.objects
        .select_related("kecamatan")
        .order_by(
            "kecamatan__nama",
            "nama"
        )
    )
    if search:
        qs = qs.filter(
            nama__icontains=search
        )
    return list(
        qs.values(
            "id",
            "nama",
            "latitude",
            "longitude",
            "kecamatan__nama",
        )
    )