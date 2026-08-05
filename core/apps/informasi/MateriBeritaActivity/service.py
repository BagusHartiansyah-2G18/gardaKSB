from core.apps.informasi.MateriBerita.models import MateriBerita
from core.apps.informasi.MateriBeritaActivity.models import MateriBeritaActivity
from django.db.models import Count, Exists, OuterRef
from core.apps.accounts.User.models import User 

from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models.functions import ExtractMonth 

def getUserLike(request,idBerita):
    if not request.user.is_authenticated:
        return 0
    return MateriBeritaActivity.objects.filter(
        materi_id=idBerita,
        aktivitas="LIKE",
        user=request.user
    ).count()
