from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from core.apps.keuangan.models import Pendapatan
from core.apps.usaha.models import JenisUsaha,ListUsaha
from core.apps.kelompok.models import Kelompok
from django.shortcuts import get_object_or_404



@login_required
def pkeuangan(request, id): 
    
    kelompok = get_object_or_404(Kelompok, id=id)  
    qs = Pendapatan.objects.select_related(
        'usaha',
        'usaha__kelompok',
        'usaha__jenisUsaha'
    ).filter(
        usaha__kelompok_id=id  # ✅ filter disini
    ).order_by('-dateCreate')


    # ✅ SEARCH
    search = request.GET.get('q')
    if search:
        qs = qs.filter(
            Q(usaha__kelompok__nmKelo__icontains=search) |
            Q(usaha__jenisUsaha__nmJUsaha__icontains=search)
        )

    # ✅ PAGINATION
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/keuangan.html', {
        'data': page_obj,
        'kelompok':kelompok,
        'search': search
        }
    )
    

@login_required
def pkeuanganAdd(request):

    usaha_list = ListUsaha.objects.select_related('kelompok')

    if request.method == "POST":
        Pendapatan.objects.create(
            usaha_id=request.POST.get('usaha'),
            dateCreate=request.POST.get('tanggal'),
            pendapatan=request.POST.get('pendapatan'),
            pengeluaran=request.POST.get('pengeluaran'),
            laba=request.POST.get('laba'),
            kas=request.POST.get('kas'),
            keterangan=request.POST.get('keterangan'),
        )
        return redirect('/pendapatan')

    return render(request, 'dashboard/keuanganAdd.html', {
        'usaha_list': usaha_list
    })

 

