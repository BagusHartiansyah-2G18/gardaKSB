from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from core.apps.kelompok.models import Kelompok,LegalitasKelompok,AnggotaKelompok,AsetKelompok
from core.apps.usaha.models import ListUsaha
from core.apps.legalitas.models import ItemLegalitas

from django.contrib.auth.decorators import login_required

from core.utils import getWilaya,isakses
from datetime import date

@login_required
def pkelompok(request, jenis):

    qs = (
        Kelompok.objects
        .select_related(
            'desa',
            'desa__kecamatan'
        )
        .filter(
            jenisKelompok__iexact=jenis
        )
    )

    search = request.GET.get('q')

    if search:
        qs = qs.filter(
            Q(nmKelo__icontains=search) |
            Q(desa__nmDesa__icontains=search)
        )
    if request: 
        wilayah = getWilaya(request)

        if wilayah:
            qs = qs.filter(
                    Q(
                        desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()     

    paginator = Paginator(qs.order_by('nmKelo'), 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(
        page_number
    ) 
    return render(
        request,
        'dashboard/kelompok.html',
        {
            'data': page_obj,
            'search': search,
            'lembaga': jenis
        }
    )
 
 
@login_required

def pkelompokDetail(request, id):

    qs = Kelompok.objects.select_related(
        'desa',
        'desa__kecamatan'
    )

    wilayah = getWilaya(request)

    if wilayah:
        qs = qs.filter(
            Q(
                desa_id__in=wilayah["desa_ids"]
            ) |
            Q(
                id__in=wilayah["kelompok_ids"]
            )
        ).distinct()

    kelompok = get_object_or_404(
        qs,
        id=id
    )

    
    item_legalitas = ItemLegalitas.objects.filter(
        idJLega__iexact=kelompok.jenisKelompok
    ) 
    legalitas_map = {
        x.itemLegalitas_id: x
        for x in LegalitasKelompok.objects.select_related(
            'itemLegalitas'
        ).filter(
            kelompok=kelompok
        )
    }

    legalitas = []

    for item in item_legalitas:
        legalitas.append({
            'item': item,
            'data': legalitas_map.get(item.id)
        })
    print(legalitas_map)

    anggota = AnggotaKelompok.objects.filter(
        kelompok=kelompok
    )

    aset = AsetKelompok.objects.filter(
        kelompok=kelompok
    )

    listUsaha = ListUsaha.objects.filter(
        kelompok=kelompok
    ) 
    return render(
        request,
        'dashboard/kelompokDetail.html',
        {
            'kelompok': kelompok,
            'legalitas': legalitas,
            'anggota': anggota,
            'aset': aset,
            'listUsaha': listUsaha,
            'isakses': isakses(request)
        }
    )



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

    obj = get_object_or_404(
        LegalitasKelompok,
        id=id
    )

    if request.method == "POST":

        try:

            status = request.POST.get(
                'status'
            )

            ket = request.POST.get(
                'keterangan',
                ''
            ).strip()

            # Jika ditolak wajib isi keterangan
            if status == '0' and not ket:

                messages.error(
                    request,
                    "❌ Keterangan wajib diisi jika status ditolak."
                )

                return redirect(
                    request.META.get(
                        'HTTP_REFERER'
                    )
                )

            if key == 'aprovalPengawal':

                obj.aprovalPengawal = (
                    status == '1'
                )

                obj.ketPengawal = ket
                obj.tglPengawal = date.today()

            elif key == 'aprovalDesa':

                obj.aprovalDesa = (
                    status == '1'
                )

                obj.ketDesa = ket
                obj.tglDesa = date.today()

            elif key == 'aprovalKec':

                obj.aprovalKec = (
                    status == '1'
                )

                obj.ketKec = ket
                obj.tglKec = date.today()

            obj.save()

            messages.success(
                request,
                "✅ Data berhasil disimpan."
            )

        except Exception as e:

            messages.error(
                request,
                f"❌ Gagal: {str(e)}"
            )

    return redirect(
        request.META.get(
            'HTTP_REFERER'
        )
    )

