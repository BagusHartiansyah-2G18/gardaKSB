from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login

from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response

# from core.apps.wilayah.models import Kecamatan, Desa
# from core.apps.usaha.models import JenisUsaha,ListUsaha
# from core.apps.legalitas.models import ItemLegalitas

# from core.apps.kelompok.models import Kelompok,AsetKelompok,LegalitasKelompok,WilayahPengawas
# from core.apps.keuangan.models import Pendapatan

# from core.apps.keuangan.vkeuangan import pkeuangan
# from core.apps.kelompok.vkelompok import pkelompokDetail

from django.http import JsonResponse

from django.utils import timezone
import pandas as pd
from django.core.paginator import Paginator

import json



from django.db.models import Q,Count
# from core.utils import summaryDashboard,summaryApproval,chartApprovalModul,chartPendAll,chartPendBulanan,summaryLegalitas,chartKelengkapan,summaryAset,chartKondisiAset,chartLembaga,chartKelompok,chartAsetKelompok,warningApproval,summaryAnggota,chartStatusKelompok,getWilaya,chartPendJUsaha,send,subMenu
from core.apps.informasi.MateriBerita.service import getRandom_berita,getBeritaPerBulan,getMateriPerBidang,getPartisipasiMateri,getBeritaON,getDetailBerita,getFileMateriPerBidang
from core.apps.pengaduan.service import getMapKasus,getGrafikJenisKasus,generateNomorTiket
from core.apps.master.Desa.service import getDesa
from core.utilsData import PARTNERS


from core.apps.pengaduan.models import Pengaduan
from core.apps.pengaduan.PengaduanHistory.models import PengaduanHistory

def home(request): 
    return render(request, 'publik/home.html', {
        'dberita': getRandom_berita(kategori="BERITA"),
        'dmateri': getRandom_berita(),
        'gberita':getBeritaPerBulan(kategori="BERITA"),
        'gmateri':getMateriPerBidang(),
        'pmateri':getPartisipasiMateri(),
        'pberita':getPartisipasiMateri(kategori="BERITA"),
        'dpatner':PARTNERS,
        "dmap": json.dumps(
            getMapKasus(),
            default=str
        )
    })
def pengaduan(request):
    return render(request, 'publik/pengaduan.html', {
        'gjenisKasus':  json.dumps(
            getGrafikJenisKasus(),
            default=str
        ),
        "dmap": json.dumps(
            getMapKasus(),
            default=str
        ),
        'ddesa':getDesa()
    })



def kirimPengaduan(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "Method tidak diizinkan"
            },
            status=405
        )

    try:
        # for key, value in request.POST.items():
        #     print(key, "=", value)
            
        pengaduan = Pengaduan.objects.create(
            nomor_tiket=generateNomorTiket(),
            judul=request.POST.get("judul"),
            desa_id=request.POST.get("desa"),
            lokasi_kejadian=request.POST.get(
                "lokasi_kejadian"
            ),
            latitude=request.POST.get(
                "latitude"
            ) or None,
            longitude=request.POST.get(
                "longitude"
            ) or None,
            nama_pelapor=request.POST.get(
                "nama"
            ),
            hp_pelapor=request.POST.get(
                "hp"
            ),
            email_pelapor=request.POST.get(
                "email"
            ) or "",
            alamat_pelapor="",
            uraian=request.POST.get(
                "uraian"
            ),
            lampiran=request.FILES.get("lampiran"),
            waktu_kejadian=timezone.now(),
            status="BARU",
            source="WEB",
        )

        PengaduanHistory.objects.create(
            pengaduan=pengaduan,
            user=None,
            judul="Pengaduan Dibuat",
            deskripsi="Pengaduan berhasil dikirim melalui portal publik.",
            status_lama="",
            status_baru="BARU",
            latitude=pengaduan.latitude,
            longitude=pengaduan.longitude
        )

        return JsonResponse(
            {
                "success": True,
                "message": "Pengaduan berhasil dikirim.",
                "nomor_tiket": pengaduan.nomor_tiket,
                "id": pengaduan.id,
            }
        )

    except Exception as e:

        return JsonResponse(
            {
                "success": False,
                "message": str(e)
            },
            status=400
        )

def trackingPengaduan(
        request,
        nomor_tiket
    ):

    pengaduan = (
        Pengaduan.objects
            .filter(
                nomor_tiket = nomor_tiket
            )
            .first()
    )

    if not pengaduan:

        return JsonResponse({
            "success": False,
            "message": "Nomor tiket tidak ditemukan."
        })

    history = list(

        PengaduanHistory.objects

            .filter(
                pengaduan = pengaduan
            )

            .values(
                "judul",
                "deskripsi",
                "status_lama",
                "status_baru",
                "created_at"
            )

            .order_by(
                "-created_at"
            )

    )

    return JsonResponse({

        "success": True,

        "pengaduan": {
            "id": pengaduan.id,
            "nomor_tiket": pengaduan.nomor_tiket,
            "judul": pengaduan.judul,
            "status": pengaduan.get_status_display(),
            "lokasi_kejadian": pengaduan.lokasi_kejadian,
            "created_at": pengaduan.created_at.strftime(
                "%d/%m/%Y %H:%M"
            ),
        },

        "history": history

    })
def informasi(request, kategori="BERITA"):
    return render(request, 'publik/informasi.html', {
        'dberita': getRandom_berita(limit=3,kategori=kategori),
        'kategori':kategori,
        'dberitaAll': getBeritaON(kategori=kategori),
    })
def detailInformasi(request,slug):
    berita = getDetailBerita(slug)
    return render(
        request,'publik/informasiDetail.html',{
            'berita': berita,
            'dterkait':getRandom_berita(kategori=berita.kategori)
        }
    )

def materiBidang(request, slug, id=None):

    dmateri = getFileMateriPerBidang(
        bidang_id=slug
    )

    dmateriOn = None

    if id:

        data = getFileMateriPerBidang(
            bidang_id=slug,
            id=id
        )
        print(data)
        if data:
            dmateriOn = data[0]

    elif dmateri:

        dmateriOn = dmateri[0]

    return render(
        request,
        "publik/materi.html",
        {
            "dmateri": dmateri,
            "dmateriOn": dmateriOn,
            "bidang":slug,
        }
    )
