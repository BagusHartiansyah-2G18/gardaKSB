from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.apps.usaha.models import JenisUsaha,ListUsaha



@login_required
def pusaha(request):
    qs = ListUsaha.objects.select_related(
        'kelompok', 'kelompok__desa', 'jenisUsaha'
    ).all()

    # ✅ SEARCH multi field
    search = request.GET.get('q')
    if search:
        qs = qs.filter(
            Q(kelompok__nmKelo__icontains=search) |
            Q(jenisUsaha__nmJUsaha__icontains=search) |
            Q(komoditi__icontains=search)
        )

    # ✅ PAGINATION
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/usaha.html', {
        'data': page_obj,
        'search': search
    })
