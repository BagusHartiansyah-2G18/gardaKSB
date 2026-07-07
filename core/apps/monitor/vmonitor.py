from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from core.apps.kelompok.models import Kelompok,LegalitasKelompok,AnggotaKelompok,AsetKelompok
from core.apps.usaha.models import ListUsaha
from django.contrib.auth.decorators import login_required
from core.utils import getWilaya,chartPendBulanan,chartPendAll,chartPendJUsaha,chartKelompok,subMenu,summaryLegalitas,chartKelengkapan,chartApproval,chartDokumen,chartKelompokKurang,summaryAset,chartKondisiAset,chartKategoriAset,chartAsetKelompok,chartAsetBermasalah,summaryApproval,chartApprovalModul,chartApprovalLevel,chartPendingModul,chartKelompokPending,chartStatusKelompok
from datetime import date

@login_required
def pmonitor(request,idJLega): 
    # print(chartPendBulanan(request,jenis='UMUM',id_jlega=idJLega))
    return render(request, 'dashboard/monitor.html', {
        'chartPendBulanan': chartPendBulanan(request,jenis='UMUM',id_jlega=idJLega), 
        'chartPendAll':chartPendAll(request,jenis='UMUM',id_jlega=idJLega),
        'chartPendJUsaha':chartPendJUsaha(request,jenis='UMUM',id_jlega=idJLega),
        'chartKelompok':chartKelompok(request,id_jlega=idJLega),
        'currentJLega':idJLega,
        "aktif":chartStatusKelompok(request)
    })
 
 
@login_required
def pmonitorLegalitas(request, idJLega): 
    
    return render(request,'dashboard/monitorLegalitas.html',{
        'summary': summaryLegalitas(request,idJLega),
        'chartKelengkapan': chartKelengkapan(request,idJLega),
        'chartApproval': chartApproval(request,idJLega),
        'chartDokumen': chartDokumen(request,idJLega),
        'chartKelompokKurang': chartKelompokKurang(request,idJLega),
        'subMenu':subMenu(),
        'currentJLega':idJLega
    })




@login_required
def pmonitorAset(request, idJLega): 
    return render(request,'dashboard/monitorAset.html',{
        'summary': summaryAset(request,idJLega),
        'chartKondisi': chartKondisiAset(request,idJLega),
        'chartKategori': chartKategoriAset(request,idJLega),
        'chartKelompok': chartAsetKelompok(request,idJLega),
        'asetBermasalah': chartAsetBermasalah(request,idJLega),
        'currentJLega':idJLega
    })



@login_required
def pmonitorAproval(request, idJLega):
    
    return render(request,'dashboard/monitorApproval.html',{
        'summary': summaryApproval(request,idJLega),

        'chartApprovalModul': chartApprovalModul(request,idJLega),
        'chartApprovalLevel': chartApprovalLevel(request,idJLega),

        'chartPendingModul': chartPendingModul(request,idJLega),
        'chartKelompokPending': chartKelompokPending(request,idJLega),
        'currentJLega': idJLega
    })



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
