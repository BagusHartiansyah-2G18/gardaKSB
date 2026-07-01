from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from core.apps.keuangan.models import Pendapatan
from core.apps.usaha.models import JenisUsaha,ListUsaha
from core.apps.kelompok.models import Kelompok
from django.shortcuts import get_object_or_404
from core.utils import getWilaya,isakses
from django.db.models import Sum
from django.contrib import messages
from datetime import date

def get_kas(kelompok_id):
    terakhir = (
        Pendapatan.objects
        .filter(usaha__kelompok_id=kelompok_id)
        .order_by('-dateCreate', '-id')
        .first()
    )

    return terakhir.kas if terakhir else 0

@login_required
def pkeuangan(request, id, jenis):

    kelompok = get_object_or_404(Kelompok, id=id)

    qs = Pendapatan.objects.select_related(
        'usaha',
        'usaha__kelompok',
        'usaha__jenisUsaha'
    ).filter(
        usaha__kelompok_id=id,
        jenis=jenis
    ).order_by('-dateCreate')

    usaha = ListUsaha.objects.filter(
        kelompok=kelompok
    )

    search = request.GET.get('q')
    if search:
        qs = qs.filter(
            Q(usaha__kelompok__nmKelo__icontains=search) |
            Q(usaha__jenisUsaha__nmJUsaha__icontains=search)
        )
 
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    return render(request, 'dashboard/keuangan.html', {
        'data': page_obj,
        'kelompok': kelompok,
        'jenis': jenis,
        'search': search,
        'usaha': usaha,
        'isakses': isakses(request)
    })
    

@login_required
def pkeuanganAdd(request, id,jenis):
    kelompok = get_object_or_404(Kelompok, id=id)
    usaha = ListUsaha.objects.filter(
        kelompok=kelompok
    )

    if request.method == "POST":
        umasuk = float(request.POST.get('pendapatan') or 0)
        ukeluar = float(request.POST.get('pengeluaran') or 0)

        if jenis != "UMUM":
            if ukeluar > umasuk:
                messages.error(
                    request,
                    f"Nominal pengeluaran melebihi kas pendapatan untuk {jenis}"
                )
                return redirect(request.path)
            else:
                umasuk = 0 

        Pendapatan.objects.create(
            usaha_id=request.POST.get('usaha'),
            dateCreate=request.POST.get('tanggal'),
            pendapatan=umasuk,
            pengeluaran=ukeluar, 
            keterangan=request.POST.get('keterangan'),
            jenis=jenis
        )
        # recalculate_kas(id)

        return redirect('pendapatan', id=kelompok.id, jenis=jenis)

    return render(request, 'dashboard/keuanganAdd.html', {
        'kelompok': kelompok,
        'usaha': usaha,
        'jenis':jenis, 
        'ukas':get_kas(id)
    })


@login_required
def pkeuanganEdit(request, id,jenis): 
    data = get_object_or_404(
        Pendapatan.objects.select_related(
            'usaha',
            'usaha__kelompok'
        ),
        id=id
    )
    data.total = (data.pengeluaran or 0) + (data.kas or 0)
    usaha = ListUsaha.objects.filter(
        kelompok=data.usaha.kelompok
    )


    if request.method == "POST":
        umasuk = float(request.POST.get('pendapatan') or 0)
        ukeluar = float(request.POST.get('pengeluaran') or 0) 
        if jenis != "UMUM":
            if ukeluar > umasuk:
                messages.error(
                    request,
                    f"Nominal pengeluaran melebihi kas pendapatan untuk {jenis}"
                )
                return redirect(request.path)
            else:
                umasuk = 0 
        
        data.usaha_id = request.POST.get('usaha')
        data.dateCreate = request.POST.get('tanggal')
        data.pendapatan=umasuk
        data.pengeluaran=ukeluar 
        
        data.save() 
        return redirect(
            'pendapatan',
            id=data.usaha.kelompok.id,
            jenis=jenis
        )

    return render(request, 'dashboard/keuanganEdit.html', {
        'data': data,
        'usaha': usaha,
        'jenis':jenis, 
    })




@login_required
def pendapatanApprove(request, id, key):
    obj = get_object_or_404(Pendapatan, id=id)
    if request.method == "POST":
        status = request.POST.get('status')
        ket = request.POST.get('keterangan')

        if key == 'pengawal':
            obj.aprovalPengawal = (status == '1')
            obj.ketPengawal = ket
            obj.tglPengawal = date.today()

        elif key == 'desa':
            obj.aprovalDesa = (status == '1')
            obj.ketDesa = ket
            obj.tglDesa = date.today()

        elif key == 'kec':
            obj.aprovalKec = (status == '1')
            obj.ketKec = ket
            obj.tglKec = date.today()
        

        obj.save()
    return redirect(request.META.get('HTTP_REFERER'))
