from django.shortcuts import render,redirect

from django.contrib.auth import authenticate, login as auth_login

from django.core.paginator import Paginator
from django.contrib import messages
from core.apps.kelompok.models import Kelompok


def pkelompok(request): 
    qs = Kelompok.objects.select_related('desa', 'desa__kecamatan').all()

    
    search = request.GET.get('q')
    if search:
        qs = qs.filter(nmKelo__icontains=search)

    # ✅ PAGINATION
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/kelompok.html', {
        'data': page_obj,
        'search': search
    })
 
 
def kelompok_detail(request, id):
    kelompok = get_object_or_404(Kelompok.objects.select_related('desa', 'desa__kecamatan'), id=id)

    legalitas = LegalitasKelompok.objects.select_related(
        'itemLegalitas'
    ).filter(kelompok=kelompok)

    return render(request, 'kelompok/detail.html', {
        'kelompok': kelompok,
        'legalitas': legalitas
    })
