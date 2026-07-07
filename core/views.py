from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login

from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.apps.wilayah.models import Kecamatan, Desa
from core.apps.usaha.models import JenisUsaha,ListUsaha
from core.apps.legalitas.models import ItemLegalitas

from core.apps.kelompok.models import Kelompok,AsetKelompok,LegalitasKelompok,WilayahPengawas
from core.apps.keuangan.models import Pendapatan

from core.apps.keuangan.vkeuangan import pkeuangan
from core.apps.kelompok.vkelompok import pkelompokDetail

from django.http import JsonResponse

import pandas as pd


from django.db.models import Q,Count
from core.utils import summaryDashboard,summaryApproval,chartApprovalModul,chartPendAll,chartPendBulanan,summaryLegalitas,chartKelengkapan,summaryAset,chartKondisiAset,chartLembaga,chartKelompok,chartAsetKelompok,warningApproval,summaryAnggota,chartStatusKelompok,getWilaya,chartPendJUsaha
 
def home(request):
    data =  [
        {
            "nama": "Kelompok Nelayan",
            "deskripsi": "Kelompok masyarakat yang melakukan penangkapan ikan di laut",
            "url": "https://png.pngtree.com/png-vector/20211015/ourlarge/pngtree-fishing-logo-png-image_3984708.png"
        },
        {
            "nama": "Pokdakan",
            "deskripsi": "Kelompok pembudidaya ikan (kolam, tambak, keramba)",
            "url": "https://1.bp.blogspot.com/-PAwtbR5Xp7Y/X2oXKU1fnCI/AAAAAAAALP0/P0NLN2cSKeoV1dUnl0lvQIr-1yQD_qc_ACNcBGAsYHQ/s400/LOGO%2BPOKDAKAN.jpg"
        },
        {
            "nama": "Poklahsar",
            "deskripsi": "Kelompok pengolah dan pemasaran hasil perikanan",
            "url": "https://img.icons8.com/color/96/fish-food.png"
        },
        {
            "nama": "Kelompok Usaha Bersama (KUB)",
            "deskripsi": "Kelompok usaha ekonomi bersama bidang perikanan",
            "url": "https://2.bp.blogspot.com/-XBzyP9GMol8/Vte34zUu-MI/AAAAAAAAEAo/-KNK48jOhrkOE1xyqPOj-iv3p1bxF5kQg/w1200-h630-p-k-no-nu/DUTA%2BLAUT.jpg"
        },
        {
            "nama": "Pokmaswas",
            "deskripsi": "Kelompok masyarakat pengawas kegiatan kelautan dan perikanan",
            "url": "https://img.icons8.com/color/96/shield.png"
        }
    ] 

    return render(request, 'publik/home.html', {
        'features': data,
        'chartLembaga': chartLembaga(request),
        'chartKelompok': chartKelompok(request),
        
        'chartPendBulanan': chartPendBulanan(request),
        'chartPendJUsaha':chartPendJUsaha(request,jenis='UMUM'),
        'chartKelengkapan': chartKelengkapan(request),

        "aktif":chartStatusKelompok(request),
        'summaryLegalitas': summaryLegalitas(request),




    })
def login(request):
    return render(request, 'publik/login.html', {
        'features': []
    })


def ajaxItemLegalitas(request):

    kelompok_id = request.GET.get(
        'kelompok_id'
    )

    data = []

    if kelompok_id:

        try:

            kelompok = Kelompok.objects.get(
                pk=kelompok_id
            )

            data = list(
                ItemLegalitas.objects.filter(
                    idJLega__iexact=
                    kelompok.jenisKelompok
                ).values(
                    'id',
                    'nmILega'
                )
            )

        except Kelompok.DoesNotExist:
            pass

    return JsonResponse(
        data,
        safe=False
    )


@login_required
def dashboard(request):   
    return render(request,'dashboard/dashboard.html',{

        'summary': summaryDashboard(request),
        'summaryApproval': summaryApproval(None,request),

        'chartApprovalModul': chartApprovalModul(None,request),

        'chartPendAll': chartPendAll(None,None,None,request),
        'chartPendBulanan': chartPendBulanan(request),

        'summaryLegalitas': summaryLegalitas(request),
        'chartPendJUsaha':chartPendJUsaha(request,jenis='UMUM'),

        'chartKelengkapan': chartKelengkapan(request),

        'summaryAset': summaryAset(request),
        'chartKondisiAset': chartKondisiAset(request),

        'chartLembaga': chartLembaga(request),

        'chartKelompok': chartKelompok(request),
        'chartAsetKelompok': chartAsetKelompok(request),

        'warningApproval': warningApproval(request),

        'totalAnggota': summaryAnggota(request),
        'warnings':earlyWarning(request),
        "aktif":chartStatusKelompok(request)
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  # ganti ke url kamu
        else:
            messages.error(request, 'Username atau password salah')

    return render(request, 'publik/login.html')

@login_required
def early(request):
    return render(request,'dashboard/earlyWarning.html',{
        'warnings':earlyWarning(request)
    })



from django.urls import reverse

def earlyWarning(request):

    data = []
 

    aset_qs = AsetKelompok.objects.all()
    pendapatan_qs = Pendapatan.objects.all()
    legalitas_qs = LegalitasKelompok.objects.all()

    if request: 
        wilayah = getWilaya(request)

        if wilayah:
            aset_qs = aset_qs.filter(
                    Q(
                        kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()    
            pendapatan_qs = pendapatan_qs.filter(
                    Q(
                        usaha__kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        usaha__kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()  
            legalitas_qs = legalitas_qs.filter(
                    Q(
                        kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()   
    if aset_qs.filter(
        kondisi='rusak'
    ).exists():

        data.append({
            'level': 'danger',
            'judul': 'Aset Rusak',
            'pesan': 'Terdapat aset dengan kondisi rusak.',
            'url': reverse(
                'pmonitorAset',
                args=['BUMDES']
            )
        })

    rugi = (
        pendapatan_qs
        .filter(
            laba__lt=0,
            jenis='UMUM'
        )
        .select_related(
            'usaha',
            'usaha__kelompok'
        )
        .first()
    )

    if rugi:

        data.append({
            'level': 'danger',
            'judul': 'Usaha Mengalami Kerugian',
            'pesan': (
                f'{rugi.usaha.kelompok.nmKelo} '
                f'mengalami laba negatif.'
            ),
            'url': reverse(
                'pkeuangan',
                args=[
                    rugi.usaha.kelompok.id,
                    'UMUM'
                ]
            )
        })

    pending = (
        legalitas_qs
        .filter(
            aprovalKec=False
        )
        .select_related(
            'kelompok'
        )
        .first()
    )

    if pending:

        data.append({
            'level': 'warning',
            'judul': 'Approval Legalitas',
            'pesan': (
                f'{pending.kelompok.nmKelo} '
                f'belum disetujui.'
            ),
            'url': reverse(
                'kelompok_detail',
                args=[pending.kelompok.id]
            )
        })

    return data

@api_view(['GET'])
def seed_sumbawa(request):
    # KECAMATAN
    # data_kecamatan = [
    #     {"id": 1, "nmKec": "Jereweh"},
    #     {"id": 2, "nmKec": "Taliwang"},
    #     {"id": 3, "nmKec": "Seteluk"},
    #     {"id": 4, "nmKec": "Sekongkang"},
    #     {"id": 5, "nmKec": "Brang Rea"},
    #     {"id": 6, "nmKec": "Poto Tano"},
    #     {"id": 7, "nmKec": "Brang Ene"},
    #     {"id": 8, "nmKec": "Maluk"},
    # ]

    # for kec in data_kecamatan:
    #     Kecamatan.objects.update_or_create(
    #         id=kec["id"],
    #         defaults={"nmKec": kec["nmKec"]}
    #     )

    # # DESA (sebagian contoh, bisa kamu tambah full)
    # data_desa = [
        
    # {"nmDesa": "Kiantar", "kecamatan_id": 6},
    # {"nmDesa": "Kokarlian", "kecamatan_id": 6},
    # {"nmDesa": "Mantar", "kecamatan_id": 6},
    # {"nmDesa": "Poto Tano", "kecamatan_id": 6},
    # {"nmDesa": "Senayan", "kecamatan_id": 6},
    # {"nmDesa": "Tambak Sari", "kecamatan_id": 6},
    # {"nmDesa": "Tebo", "kecamatan_id": 6},
    # {"nmDesa": "Tuananga", "kecamatan_id": 6}

    # ]

    # for desa in data_desa:
    #     Desa.objects.update_or_create(
    #         nmDesa=desa["nmDesa"],
    #         kecamatan_id=desa["kecamatan_id"]
    #     )

    

    # return Response({"message": "Data Sumbawa Barat inserted ✅"})
    # data = [
    #     "Penangkapan",
    #     "Pengolahan",
    #     "Pembesaran",
    #     "Pemasaran Hasil Laut",
    #     "Budidaya",
    #     "Pengawasan dan pelestarian",
    # ]

    # inserted = []
    # skipped = []

    # for item in data:
    #     obj, created = JenisUsaha.objects.get_or_create(
    #         nmJUsaha=item.strip().title()
    #     )
    #     if created:
    #         inserted.append(item)
    #     else:
    #         skipped.append(item)

    # return Response({
    #     "inserted": inserted,
    #     "skipped": skipped,
    #     "total_inserted": len(inserted)
    # })
    
    # desa_map = {
    #     "Senayan": 50,
    #     "Kiantar": 46,
    #     "Poto Tano": 49,
    #     "Poto tano": 49,
    #     "Tambak sari": 51,
    #     "Tambak Sari": 51,
    #     "Kokarlian": 47,
    #     "Tebo": 52,
    #     "Tua nanga": 53,
    #     "Tuananga": 53,
    # }

    # data = [
    #     # Senayan
    #     {"nmKelo": "KUB Poto Gili", "desa": "Senayan", "kelas": "Madya", "ketua": "Syarifuddin Arirs", "koordinat": ""},
    #     {"nmKelo": "Poklahsar Sepakek Barokah", "desa": "Senayan", "kelas": "Pemula", "ketua": "Fatmawati", "koordinat": ""},
    #     {"nmKelo": "Jorok Aer", "desa": "Senayan", "kelas": "Pemula", "ketua": "M. Zain Lubis", "koordinat": "-8.618196,116.857232"},

    #     # Kiantar
    #     {"nmKelo": "KUB Pendi Jangi", "desa": "Kiantar", "kelas": "Madya", "ketua": "Mustaram", "koordinat": "-8.592626,116.797773"},
    #     {"nmKelo": "KUB Tari Pemendi", "desa": "Kiantar", "kelas": "Madya", "ketua": "Abu Bakar M", "koordinat": ""},
    #     {"nmKelo": "KUB Balong Niat", "desa": "Kiantar", "kelas": "Pemula", "ketua": "Hasbullah", "koordinat": ""},
    #     {"nmKelo": "KUB Saling Pariri", "desa": "Kiantar", "kelas": "Pemula", "ketua": "Burhanuddin", "koordinat": ""},
    #     {"nmKelo": "Pokdakan Sagena Bahari", "desa": "Kiantar", "kelas": "Madya", "ketua": "Syarifuddin P", "koordinat": "-8.580129,116.816388"},
    #     {"nmKelo": "Gapokkan Sagena Sejahtera", "desa": "Kiantar", "kelas": "Pemula", "ketua": "Alfian", "koordinat": "-8.580675,116.813514"},
    #     {"nmKelo": "Pokdakan Pendi Jangi", "desa": "Kiantar", "kelas": "Pemula", "ketua": "Basaruddin", "koordinat": "-8.580901,116.813304"},
    #     {"nmKelo": "Poklahsar Karya Makmur", "desa": "Kiantar", "kelas": "Pemula", "ketua": "Ninik Lestari", "koordinat": ""},
    #     {"nmKelo": "Koperasi Serba Usaha Sagena Mandiri Sejahtera", "desa": "Kiantar", "kelas": "Pemula", "ketua": "Alfian", "koordinat": ""},
    #     {"nmKelo": "Sinar Bahari", "desa": "Kiantar", "kelas": "Pemula", "ketua": "Saripuddin", "koordinat": "-8.581327,116.832145"},

    #     # Poto Tano
    #     {"nmKelo": "KUB Usaha Mandiri", "desa": "Poto Tano", "kelas": "Madya", "ketua": "Margauddin", "koordinat": "-8.528424,116.832260"},
    #     {"nmKelo": "KUB Kakap Merah", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Najamuddin", "koordinat": "-8.530699,116.832078"},
    #     {"nmKelo": "KUB Kuda Laut", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Kamaruddin B", "koordinat": "-8.530619,116.833139"},
    #     {"nmKelo": "KUB Baci Lestari", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Madahu", "koordinat": "-8.528489,116.831742"},
    #     {"nmKelo": "KUB Bahari Abadi", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Marzuki", "koordinat": "-8.528265,116.832133"},
    #     {"nmKelo": "KUB Citra Bahari", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Mansaha", "koordinat": "-8.529516,116.831766"},
    #     {"nmKelo": "KUB Laut Biru", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Suharli", "koordinat": "-8.527658,116.832237"},
    #     {"nmKelo": "KUB Maju Indah", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Manaku", "koordinat": "-8.529558,116.832728"},
    #     {"nmKelo": "KUB Napoleon", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Agustino", "koordinat": "-8.527828,116.832348"},
    #     {"nmKelo": "KUB Pembaharuan", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Sudirman", "koordinat": "-8.526633,116.831693"},
    #     {"nmKelo": "KUB Perubahan", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Manajai", "koordinat": "-8.527303,116.831851"},
    #     {"nmKelo": "KUB Sikase Ase", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Samarollah", "koordinat": "-8.52883,116.832399"},
    #     {"nmKelo": "Tano Jaya", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Hadijah", "koordinat": "-8.5277940,116.832145"},
    #     {"nmKelo": "KUB Pelita Poto Tano", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Mahari", "koordinat": ""},
    #     {"nmKelo": "KUB Jaring Maero", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Mustar", "koordinat": ""},
    #     {"nmKelo": "Poklahsar Persatuan Pasir Putih", "desa": "Poto Tano", "kelas": "Pemula", "ketua": "Yuliana", "koordinat": ""},

    #     # Tambak Sari
    #     {"nmKelo": "Pemuda Perubahan", "desa": "Tambak Sari", "kelas": "Pemula", "ketua": "Saepul Haq", "koordinat": "-8.564049,116.842005"},
    #     {"nmKelo": "KUB Plasma", "desa": "Tambak Sari", "kelas": "Pemula", "ketua": "Margana", "koordinat": "-8.567836,118.842697"},

    #     # Kokarlian
    #     {"nmKelo": "Pokdakan Sekar Bahari", "desa": "Kokarlian", "kelas": "Madya", "ketua": "Ibnul Irsal", "koordinat": "-8.538898,116.856802"},
    #     {"nmKelo": "Pokdakan Samudera", "desa": "Kokarlian", "kelas": "Madya", "ketua": "Muhammad Rojik", "koordinat": "-8.538903,116.856037"},

    #     # Tebo
    #     {"nmKelo": "Penyare", "desa": "Tebo", "kelas": "Pemula", "ketua": "Syarifuddin", "koordinat": "-8.608167,116.860619"},

    #     # Tuananga
    #     {"nmKelo": "Pokdakan Bangka Bella", "desa": "Tuananga", "kelas": "Pemula", "ketua": "Samsuddin", "koordinat": ""},
    #     {"nmKelo": "Pokdakan Bukit Kenangan", "desa": "Tuananga", "kelas": "Pemula", "ketua": "Muhatadim", "koordinat": ""},
    #     {"nmKelo": "Pokdakan Maju Jaya", "desa": "Tuananga", "kelas": "Pemula", "ketua": "Jayadi", "koordinat": ""},
    #     {"nmKelo": "Pokdakan Niat Balong", "desa": "Tuananga", "kelas": "Pemula", "ketua": "Syafruddin", "koordinat": ""},
    #     {"nmKelo": "Poklahsar Karya Tani", "desa": "Tuananga", "kelas": "Pemula", "ketua": "Timor Yati", "koordinat": ""},
    #     {"nmKelo": "Pokdakan Sama Maras", "desa": "Tuananga", "kelas": "Pemula", "ketua": "Emil", "koordinat": ""},
    #     {"nmKelo": "Pokdakan Saruruk Bangkit", "desa": "Tuananga", "kelas": "Madya", "ketua": "Zainudin", "koordinat": ""},
    #     {"nmKelo": "Saruruk Maju", "desa": "Tuananga", "kelas": "Pemula", "ketua": "Suldim", "koordinat": ""},
    #     {"nmKelo": "Maronge Barokah", "desa": "Tuananga", "kelas": "Pemula", "ketua": "Saparuddin", "koordinat": ""},
    #     {"nmKelo": "Anugerah Laut", "desa": "Tuananga", "kelas": "Pemula", "ketua": "M. Sabur", "koordinat": ""},
    #     {"nmKelo": "Saling Sakiki", "desa": "Tuananga", "kelas": "Pemula", "ketua": "Asanul", "koordinat": ""},
    #     {"nmKelo": "Limung Prapat", "desa": "Tuananga", "kelas": "Pemula", "ketua": "Andi Aziz", "koordinat": ""},
    #     {"nmKelo": "Ingat Bersama", "desa": "Tuananga", "kelas": "Pemula", "ketua": "A. Haris Hamid", "koordinat": ""},
    #     {"nmKelo": "Pokmaswas Bangka Bela", "desa": "Tuananga", "kelas": "Pemula", "ketua": "Zakaria", "koordinat": ""},
    # ]


    # inserted = []
    # skipped = []
    # errors = []

    
    # for item in data:

    #     nama = item["desa"].strip()

    #     desa = Desa.objects.filter(
    #         Q(nmDesa__iexact=nama) |
    #         Q(nmDesa__icontains=nama)
    #     ).first()
 
    #     if not desa:
    #         errors.append(f"Desa tidak ditemukan: {nama}")
    #         continue

    #     try:
    #         obj, created = Kelompok.objects.get_or_create(
    #             nmKelo=item["nmKelo"],
    #             desa=desa,
    #             defaults={
    #                 "kelas": item["kelas"],
    #                 "ketua": item["ketua"],
    #                 "koordinat": item["koordinat"]
    #             }
    #         )

    #         if created:
    #             inserted.append(item["nmKelo"])
    #         else:
    #             skipped.append(item["nmKelo"])

    #     except Exception as e:
    #         errors.append(str(e))


    # return Response({
    #     "inserted": inserted,
    #     "skipped": skipped,
    #     "errors": errors
    # })
    # [{'id': 1, 'nmJUsaha': 'Penangkapan'}, {'id': 2, 'nmJUsaha': 'Pengolahan'}, {'id': 3, 'nmJUsaha': 'Pembesaran'}, {'id': 4, 'nmJUsaha': 'Pemasaran Hasil Laut'}, {'id': 5, 'nmJUsaha': 'Budidaya'}, {'id': 6, 'nmJUsaha': 'Pengawasan Dan Pelestarian'}]
    # [{'id': 1, 'nmKelo': 'KUB Poto Gili', 'ketua': 'Syarifuddin Arirs'}, {'id': 2, 'nmKelo': 'Poklahsar Sepakek Barokah', 'ketua': 'Fatmawati'}, {'id': 3, 'nmKelo': 'Jorok Aer', 'ketua': 'M. Zain Lubis'}, {'id': 4, 'nmKelo': 'KUB Pendi Jangi', 'ketua': 'Mustaram'}, {'id': 5, 'nmKelo': 'KUB Tari Pemendi', 'ketua': 'Abu Bakar M'}, {'id': 6, 'nmKelo': 'KUB Balong Niat', 'ketua': 'Hasbullah'}, {'id': 7, 'nmKelo': 'KUB Saling Pariri', 'ketua': 'Burhanuddin'}, {'id': 8, 'nmKelo': 'Pokdakan Sagena Bahari', 'ketua': 'Syarifuddin P'}, {'id': 9, 'nmKelo': 'Gapokkan Sagena Sejahtera', 'ketua': 'Alfian'}, {'id': 10, 'nmKelo': 'Pokdakan Pendi Jangi', 'ketua': 'Basaruddin'}, {'id': 11, 'nmKelo': 'Poklahsar Karya Makmur', 'ketua': 'Ninik Lestari'}, {'id': 12, 'nmKelo': 'Koperasi Serba Usaha Sagena Mandiri Sejahtera', 'ketua': 'Alfian'}, {'id': 13, 'nmKelo': 'Sinar Bahari', 'ketua': 'Saripuddin'}, {'id': 14, 'nmKelo': 'KUB Usaha Mandiri', 'ketua': 'Margauddin'}, {'id': 15, 'nmKelo': 'KUB Kakap Merah', 'ketua': 'Najamuddin'}, {'id': 16, 'nmKelo': 'KUB Kuda Laut', 'ketua': 'Kamaruddin B'}, {'id': 17, 'nmKelo': 'KUB Baci Lestari', 'ketua': 'Madahu'}, {'id': 18, 'nmKelo': 'KUB Bahari Abadi', 'ketua': 'Marzuki'}, {'id': 19, 'nmKelo': 'KUB Citra Bahari', 'ketua': 'Mansaha'}, {'id': 20, 'nmKelo': 'KUB Laut Biru', 'ketua': 'Suharli'}, {'id': 21, 'nmKelo': 'KUB Maju Indah', 'ketua': 'Manaku'}, {'id': 22, 'nmKelo': 'KUB Napoleon', 'ketua': 'Agustino'}, {'id': 23, 'nmKelo': 'KUB Pembaharuan', 'ketua': 'Sudirman'}, {'id': 24, 'nmKelo': 'KUB Perubahan', 'ketua': 'Manajai'}, {'id': 25, 'nmKelo': 'KUB Sikase Ase', 'ketua': 'Samarollah'}, {'id': 26, 'nmKelo': 'Tano Jaya', 'ketua': 'Hadijah'}, {'id': 27, 'nmKelo': 'KUB Pelita Poto Tano', 'ketua': 'Mahari'}, {'id': 28, 'nmKelo': 'KUB Jaring Maero', 'ketua': 'Mustar'}, {'id': 29, 'nmKelo': 'Poklahsar Persatuan Pasir Putih', 'ketua': 'Yuliana'}, {'id': 30, 'nmKelo': 'Pemuda Perubahan', 'ketua': 'Saepul Haq'}, {'id': 31, 'nmKelo': 'KUB Plasma', 'ketua': 'Margana'}, {'id': 32, 'nmKelo': 'Pokdakan Sekar Bahari', 'ketua': 'Ibnul Irsal'}, {'id': 33, 'nmKelo': 'Pokdakan Samudera', 'ketua': 'Muhammad Rojik'}, {'id': 34, 'nmKelo': 'Penyare', 'ketua': 'Syarifuddin'}, {'id': 35, 'nmKelo': 'Pokdakan Bangka Bella', 'ketua': 'Samsuddin'}, {'id': 36, 'nmKelo': 'Pokdakan Bukit Kenangan', 'ketua': 'Muhatadim'}, {'id': 37, 'nmKelo': 'Pokdakan Maju Jaya', 'ketua': 'Jayadi'}, {'id': 38, 'nmKelo': 'Pokdakan Niat Balong', 'ketua': 'Syafruddin'}, {'id': 39, 'nmKelo': 'Poklahsar Karya Tani', 'ketua': 'Timor Yati'}, {'id': 40, 'nmKelo': 'Pokdakan Sama Maras', 'ketua': 'Emil'}, {'id': 41, 'nmKelo': 'Pokdakan Saruruk Bangkit', 'ketua': 'Zainudin'}, {'id': 42, 'nmKelo': 'Saruruk Maju', 'ketua': 'Suldim'}, {'id': 43, 'nmKelo': 'Maronge Barokah', 'ketua': 'Saparuddin'}, {'id': 44, 'nmKelo': 'Anugerah Laut', 'ketua': 'M. Sabur'}, {'id': 45, 'nmKelo': 'Saling Sakiki', 'ketua': 'Asanul'}, {'id': 46, 'nmKelo': 'Limung Prapat', 'ketua': 'Andi Aziz'}, {'id': 47, 'nmKelo': 'Ingat Bersama', 'ketua': 'A. Haris Hamid'}, {'id': 48, 'nmKelo': 'Pokmaswas Bangka Bela', 'ketua': 'Zakaria'}]
    # print(list(Kelompok.objects.values('id', 'nmKelo','ketua')))

    # data_usaha = [
    #     # Senayan
    #     {"kelompok": 1, "jenisUsaha": 1, "komoditi": "Ikan Laut", "wadah": "", "teknologi": "", "lahan": "", "tglMulai": "", "status": "Aktif"},
    #     {"kelompok": 2, "jenisUsaha": 2, "komoditi": "Ikan Laut", "wadah": "", "teknologi": "", "lahan": "", "tglMulai": "", "status": "Aktif"},
    #     {"kelompok": 3, "jenisUsaha": 3, "komoditi": "Nila", "wadah": "Kolam Tanah", "teknologi": "", "lahan": "810", "tglMulai": "", "status": "Aktif"},

    #     # Kiantar
    #     {"kelompok": 4, "jenisUsaha": 1, "komoditi": "Ikan Laut", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 5, "jenisUsaha": 1, "komoditi": "Ikan Laut", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 6, "jenisUsaha": 1, "komoditi": "Ikan Laut", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 7, "jenisUsaha": 1, "komoditi": "Ikan Laut", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 8, "jenisUsaha": 3, "komoditi": "Rumput Laut", "wadah": "Long Line", "teknologi": "", "lahan": "5000", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 9, "jenisUsaha": 3, "komoditi": "Rumput Laut, Kerapu, Bawal", "wadah": "Long Line, KJA", "teknologi": "", "lahan": "5000", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 10, "jenisUsaha": 3, "komoditi": "Rumput Laut, Bawal, Kerapu", "wadah": "Long Line, KJA", "teknologi": "", "lahan": "5000", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 11, "jenisUsaha": 2, "komoditi": "Ikan", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 12, "jenisUsaha": 4, "komoditi": "Rumput laut dan ikan", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 13, "jenisUsaha": 1, "komoditi": "Ikan Laut", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},

    #     # Poto Tano (contoh sebagian, sisanya pola sama Penangkapan)
    #     {"kelompok": 14, "jenisUsaha": 1, "komoditi": "Ikan laut", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 15, "jenisUsaha": 1, "komoditi": "Ikan laut", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 16, "jenisUsaha": 1, "komoditi": "Ikan laut", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 26, "jenisUsaha": 2, "komoditi": "Abon Ikan", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},

    #     # Tambak Sari
    #     {"kelompok": 30, "jenisUsaha": 3, "komoditi": "Nila", "wadah": "Kolam Terpal", "teknologi": "Semi Intensif", "lahan": "131", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 31, "jenisUsaha": 1, "komoditi": "Ikan Laut", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},

    #     # Kokarlian
    #     {"kelompok": 32, "jenisUsaha": 3, "komoditi": "Rumput Laut", "wadah": "Long Line", "teknologi": "", "lahan": "5000", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 33, "jenisUsaha": 3, "komoditi": "Rumput Laut", "wadah": "Long Line", "teknologi": "", "lahan": "5000", "status": "Aktif", "tglMulai": ""},

    #     # Tebo
    #     {"kelompok": 34, "jenisUsaha": 3, "komoditi": "Nila, Karper", "wadah": "Kolam Tanah, Kolam Beton", "teknologi": "Tradisional", "lahan": "1185", "status": "Aktif", "tglMulai": ""},

    #     # Tuananga
    #     {"kelompok": 35, "jenisUsaha": 3, "komoditi": "Rumput Laut", "wadah": "Patok Dasar", "teknologi": "", "lahan": "6.6", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 39, "jenisUsaha": 2, "komoditi": "Gurita", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 40, "jenisUsaha": 5, "komoditi": "Rumput Laut", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},
    #     {"kelompok": 48, "jenisUsaha": 6, "komoditi": "", "wadah": "", "teknologi": "", "lahan": "", "status": "Aktif", "tglMulai": ""},
    # ]
    
    # inserted = []
    # skipped = []

    # for item in data_usaha:
    #     try:
    #         obj, created = ListUsaha.objects.get_or_create(
    #             kelompok_id=item["kelompok"],
    #             jenisUsaha_id=item["jenisUsaha"],
    #             defaults={
    #                 "komoditi": item["komoditi"],
    #                 "wadah": item["wadah"],
    #                 "teknologi": item["teknologi"],
    #                 "lahan": item["lahan"],
    #                 "tglMulai": item["tglMulai"],
    #                 "status": item["status"],
    #             }
    #         )

    #         if created:
    #             inserted.append(item["kelompok"])
    #         else:
    #             skipped.append(item["kelompok"])

    #     except Exception as e:
    #         print(e)

    # return Response({
    #     "inserted": len(inserted),
    #     "skipped": len(skipped)
    # })

    return Response({
    })





