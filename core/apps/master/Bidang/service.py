from core.apps.master.Bidang.models import Bidang 
from django.db.models import Q,Count 
from django.utils import timezone   

def getBidang():

    return list(

        Bidang.objects

        .annotate(

            total_materi=Count(
                "userprofile__user__materiberita",
                filter=Q(
                    userprofile__user__materiberita__kategori="MATERI",
                    userprofile__user__materiberita__status_publish=True,
                    userprofile__user__materiberita__is_public=True
                ),
                distinct=True
            )

        )

        .values(
            "id",
            "kode",
            "nama",
            "total_materi"
        )

        .order_by("nama")

    )