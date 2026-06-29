from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from core.apps.kelompok.models import Kelompok,LegalitasKelompok,AnggotaKelompok,AsetKelompok
from core.apps.usaha.models import ListUsaha
from django.contrib.auth.decorators import login_required
from core.utils import getWilaya,isakses
from datetime import date

@login_required
def pkelompok(request):
    qs = Kelompok.objects.select_related('desa', 'desa__kecamatan').all()

    search = request.GET.get('q')
    if search:
        qs = qs.filter(
            Q(nmKelo__icontains=search) |
            Q(desa__nmDesa__icontains=search)
        )

    # ✅ filter wilayah
    desa_list = getWilaya(request)

    if desa_list is not None:
        desa_list = list(desa_list)

        if len(desa_list) > 0:
            qs = qs.filter(desa_id__in=desa_list)
        else:
            qs = qs.none()

    print("TOTAL DATA:", qs.count())

    # ✅ pagination
    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/kelompok.html', {
        'data': page_obj,
        'search': search
    })
 
 
@login_required
def pkelompokDetail(request, id):
    
    kelompok = get_object_or_404(
        Kelompok.objects.select_related('desa', 'desa__kecamatan'),
        id=id
    )

    legalitas = LegalitasKelompok.objects.select_related(
        'itemLegalitas'
    ).filter(kelompok=kelompok)

    anggota = AnggotaKelompok.objects.filter(kelompok=kelompok)

    aset = AsetKelompok.objects.filter(kelompok=kelompok)

    listUsaha = ListUsaha.objects.filter(kelompok=kelompok)

    return render(request, 'dashboard/kelompokDetail.html', {
        'kelompok': kelompok,
        'legalitas': legalitas,
        'anggota': anggota,
        'aset': aset,
        'listUsaha':listUsaha,
        'isakses':isakses(request)
    })



@login_required
def pkelompokAnggotaAdd(request, id):
    kelompok = get_object_or_404(Kelompok, id=id)

    if request.method == "POST":
        AnggotaKelompok.objects.create(
            kelompok=kelompok,
            nama=request.POST.get('nama'),
            jabatan=request.POST.get('jabatan'),
            noHp=request.POST.get('noHp'),
            alamat=request.POST.get('alamat')
        )
        return redirect('kelompok_detail', id=kelompok.id)

    return render(request, 'dashboard/kelompokanggota_add.html', {
        'kelompok': kelompok
    })


@login_required
def anggota_delete(request, id):
    anggota = get_object_or_404(AnggotaKelompok, id=id)
    kelompok_id = anggota.kelompok.id

    if request.method == "POST":
        anggota.delete()

    return redirect('kelompok_detail', id=kelompok_id)


@login_required
def pkelompoAsetAdd(request, id):
    kelompok = get_object_or_404(Kelompok, id=id)

    if request.method == "POST":
        AsetKelompok.objects.create(
            kelompok=kelompok,
            namaAset=request.POST.get('namaAset'),
            jumlah=request.POST.get('jumlah'),
            kondisi=request.POST.get('kondisi'),
            nilai=request.POST.get('nilai')
        )
        return redirect('kelompok_detail', id=kelompok.id)

    return render(request, 'dashboard/kelompokaset_add.html', {
        'kelompok': kelompok
    })


@login_required
def aset_delete(request, id):
    aset = get_object_or_404(AsetKelompok, id=id)
    kelompok_id = aset.kelompok.id

    if request.method == "POST":
        aset.delete()

    return redirect('kelompok_detail', id=kelompok_id)



@login_required
def legalitasApprove(request, id, key):
    obj = get_object_or_404(LegalitasKelompok, id=id)

    if request.method == "POST":
        try:
            status = request.POST.get('status')
            ket = request.POST.get('keterangan')

            if key == 'aprovalPengawal':
                obj.aprovalPengawal = (status == '1')
                obj.ketPengawal = ket
                obj.tglPengawal = date.today()

            elif key == 'aprovalDesa':
                obj.aprovalDesa = (status == '1')
                obj.ketDesa = ket
                obj.tglDesa = date.today()

            elif key == 'aprovalKec':
                obj.aprovalKec = (status == '1')
                obj.ketKec = ket
                obj.tglKec = date.today()

            obj.save()
        except Exception as e:
            messages.error(request, f"❌ Gagal: {str(e)}")
    return redirect(request.META.get('HTTP_REFERER'))
