
from core.apps.kelompok.models import WilayahPengawas

from django.db.models.functions import Coalesce
from django.db.models import Sum,Count,Q,F,Value ,DecimalField

from django.db.models.functions import ExtractMonth
from core.apps.kelompok.models import Kelompok,LegalitasKelompok,AnggotaKelompok,AsetKelompok
from core.apps.wilayah.models import Kecamatan, Desa 
from core.apps.usaha.models import ListUsaha

from core.apps.keuangan.models import Pendapatan 
from core.apps.legalitas.models import ItemLegalitas
import requests
import aiohttp
from aiohttp import FormData


def subMenu(request=None):

    qs = Kelompok.objects.all()

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

    return (
        qs.values( 
            idJLega=F('jenisKelompok') 
        )
        .distinct()
        .order_by(
            'jenisKelompok'
        )
    ) 
def getWilaya(request): 
    if not request.user:
        return None

    user = request.user

    if not user.is_authenticated:
        return None

    if user.is_superuser:
        return None

    wilayah = WilayahPengawas.objects.filter(
        user=user
    )

    desa_ids = []
    kelompok_ids = []

    for item in wilayah:

        if item.kelompok_id:
            kelompok_ids.append(
                item.kelompok_id
            )
        else:
            desa_ids.append(
                item.desa_id
            )

    return {
        "desa_ids": desa_ids,
        "kelompok_ids": kelompok_ids
    }

def get_wilayah_qs(request):

    qs = Kelompok.objects.all()

    wilayah = getWilaya(request)

    if not wilayah:
        return qs

    desa_ids = wilayah.get('desa_ids', [])
    kelompok_ids = wilayah.get('kelompok_ids', [])

    return qs.filter(
        Q(desa_id__in=desa_ids) |
        Q(id__in=kelompok_ids)
    ).distinct()




def send(message: str, target: str) -> bool:
    try:
        payload = {
            "target": target,
            "message": message,
            "countryCode": "62",
        }

        resp = requests.post(
            "https://api.fonnte.com/send",
            headers={
                "Authorization": "rGkDFJZnxeprGTKcV78S"
            },
            data=payload,
            timeout=30
        )

        try:
            result = resp.json()
        except Exception:
            result = {}

        print("[Fonnte]", resp.status_code, result)

        if resp.status_code >= 400 or result.get("status") is False:
            return False

        return True

    except Exception as e:
        print(e)
        return False

def filterWilayahPendapatan(qs, request=None):

    if not request:
        return qs

    wilayah = getWilaya(request)

    if wilayah:
        qs = qs.filter(
                Q(
                    usaha__kelompok__desa_id__in=wilayah["desa_ids"]
                ) |
                Q(
                    usaha__kelompok__id__in=wilayah["kelompok_ids"]
                )
            ).distinct() 
    return qs


def isakses(request):

    user = request.user

    if user.is_superuser:
        return 'KECAMATAN'

    wilayah = WilayahPengawas.objects.filter(
        user=user
    )

    # Pengawal = ada kelompok spesifik
    if wilayah.filter(
        kelompok__isnull=False
    ).exists():
        return 'PENGAWAL'

    # Desa = hanya desa
    if user.is_staff:
        return 'DESA'

    return None
    
def getFilter(jenis=None, kelompok_id=None, id_jlega=None):
    filters = {}

    if jenis:
        filters['jenis'] = jenis

    if kelompok_id:
        filters['usaha__kelompok_id'] = kelompok_id

    if id_jlega:
        filters[
            'usaha__kelompok__jenisKelompok__iexact'
        ] = id_jlega
    return filters

BULAN = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'Mei',
    6: 'Jun',
    7: 'Jul',
    8: 'Agu',
    9: 'Sep',
    10: 'Okt',
    11: 'Nov',
    12: 'Des',
}



def chartPendBulanan(
        request=None,
        jenis=None,
        kelompok_id=None,
        id_jlega=None
    ):

    filters = getFilter(
        jenis,
        kelompok_id,
        id_jlega
    ) 
     
    qs = Pendapatan.objects.filter(
        **filters
    )
     
    if request:
        wilayah = getWilaya(request)

        if wilayah:
            qs = qs.filter(
                    Q(
                        usaha__kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        usaha__kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()  

    data = (
        qs
        .annotate(
            month=ExtractMonth("dateCreate")
        )
        .values("month")
        .annotate(
            pendapatan=Sum("pendapatan"),
            pengeluaran=Sum("pengeluaran"),
            laba=Sum("laba")
        )
        .order_by("month")
    )

    hasil = []

    for item in data:

        hasil.append({
            'bulan': BULAN[item['month']],
            'pendapatan': item['pendapatan'] or 0,
            'pengeluaran': item['pengeluaran'] or 0,
            'laba': item['laba'] or 0,
        })

    return hasil





def chartPendAll(
    request=None,
    jenis=None,
    kelompok_id=None,
    id_jlega=None
):

    filters = getFilter(
        jenis,
        kelompok_id,
        id_jlega
    )

    qs = Pendapatan.objects.filter(
        **filters
    )

    qs = filterWilayahPendapatan(
        qs,
        request
    )

    return qs.aggregate(
        total_pendapatan=Sum('pendapatan'),
        total_pengeluaran=Sum('pengeluaran'),
        total_laba=Sum('laba')
    )




def chartPendJUsaha(
        request=None,
        jenis=None,
        kelompok_id=None,
        id_jlega=None
    ):

    filters = getFilter(
        jenis,
        kelompok_id,
        id_jlega
    )

    qs = Pendapatan.objects.filter(
        **filters
    )

    if request:
        wilayah = getWilaya(request)

        if wilayah:
            qs = qs.filter(
                    Q(
                        usaha__kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        usaha__kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()  

    return (
        qs.values(
            'usaha__jenisUsaha__nmJUsaha'
        )
        .annotate(
            total=Sum('pendapatan')
        )
        .order_by('-total')
    )


def chartKelompok(
        request=None,
        id_jlega=None
    ):

    filters = getFilter(
        None,
        None,
        id_jlega
    )

    qs = Pendapatan.objects.filter(
        **filters
    )

    if request:
        wilayah = getWilaya(request)

        if wilayah:
            qs = qs.filter(
                    Q(
                        usaha__kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        usaha__kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()  
    return (
        qs.values(
            'usaha__kelompok__nmKelo'
        )
        .annotate(
            total=Sum('pendapatan')
        )
        .order_by('-total')
    )

def chartApprovalAll(id_jlega=None):

    filters = getFilter(id_jlega)
    qs = Pendapatan.objects.filter(**filters)
    return {
        'pengawal': qs.filter(
            aprovalPengawal=True
        ).count(),

        'desa': qs.filter(
            aprovalDesa=True
        ).count(),

        'kecamatan': qs.filter(
            aprovalKec=True
        ).count(),

        'belum': qs.filter(
            aprovalKec=False
        ).count(),
    }

def summaryUsaha(id_jlega):
    return (
        ListUsaha.objects
        .filter(
            kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
        )
        .distinct()
        .count()
    )
def chartKelompokAll():    
    return Kelompok.objects.filter(
        legalitaskelompok__itemLegalitas__idJLega='BUMDES'
    ).distinct().count()
def chartAnggotaAll():    
    return Kelompok.objects.filter(
        legalitaskelompok__itemLegalitas__idJLega='BUMDES'
    ).distinct().count()



def summaryAset(
        request,
        id_jlega=None
    ):

    qs = AsetKelompok.objects.all()

    if id_jlega:
        qs = qs.filter(
            kelompok__jenisKelompok__iexact=id_jlega
        )
    
    if request:
        wilayah = getWilaya(request)

        if wilayah:
            qs = qs.filter(
                    Q(
                        kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()  
    return {
        'total_aset': qs.count(),

        'nilai_aset': (
            qs.aggregate(
                total=Sum('nilai')
            )['total'] or 0
        ),

        'baik': qs.filter(
            kondisi='baik'
        ).count(),

        'rusak': qs.filter(
            kondisi='rusak'
        ).count(),
    }



def chartKondisiAset(
    request,
    id_jlega=None
):

    qs = AsetKelompok.objects.all()

    if id_jlega:
        qs = qs.filter(
            kelompok__jenisKelompok__iexact=id_jlega
        )
    if request:
        wilayah = getWilaya(request)

        if wilayah:
            qs = qs.filter(
                    Q(
                        kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()   

    return {
        'baik': qs.filter(
            kondisi='baik'
        ).count(),

        'perlu': qs.filter(
            kondisi='perlu_perbaikan'
        ).count(),

        'rusak': qs.filter(
            kondisi='rusak'
        ).count()
    }



def chartKategoriAset(
    request,
    id_jlega=None
):

    qs = AsetKelompok.objects.all()

    if id_jlega:
        qs = qs.filter(
            kelompok__jenisKelompok__iexact=id_jlega
        )

    if request:
        wilayah = getWilaya(request)

        if wilayah:
            qs = qs.filter(
                    Q(
                        kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()  

    return (
        qs.values(
            'kategori'
        )
        .annotate(
            total=Count('id')
        )
        .order_by('-total')
    )





def chartAsetKelompok(
    request,
    id_jlega=None
):

    qs = AsetKelompok.objects.all()

    if id_jlega:
        qs = qs.filter(
            kelompok__jenisKelompok__iexact=id_jlega
        )

    if request:
        wilayah = getWilaya(request)

        if wilayah:
            qs = qs.filter(
                    Q(
                        kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()  

    return (
        qs.values(
            'kelompok__nmKelo'
        )
        .annotate(
            total=Coalesce(
                Sum('nilai'),
                Value(0),
                output_field=DecimalField(
                    max_digits=18,
                    decimal_places=2
                )
            )
        )
        .order_by('-total')
    )



def summaryStatusKelompok(
        request,
        id_jlega=None
    ):

    qs = Kelompok.objects.all()
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
    if id_jlega:
        qs = qs.filter(
            jenisKelompok__iexact=id_jlega
        )

    aktif = qs.filter(
        statusOperasional__iexact='Aktif'
    ).count()

    tidak_aktif = qs.filter(
        statusOperasional__iexact='Tidak Aktif'
    ).count()

    total = qs.count()

    return {
        'total': total,
        'aktif': aktif,
        'tidak_aktif': tidak_aktif,
        'persen_aktif': round(
            (aktif / total) * 100,
            1
        ) if total else 0
    }

def chartStatusKelompok(
        request=None,
        id_jlega=None
    ):

    data = summaryStatusKelompok(
        request,
        id_jlega
    )

    return {
        'labels': [
            'Aktif',
            'Tidak Aktif'
        ],
        'values': [
            data['aktif'],
            data['tidak_aktif']
        ]
    }

def chartAsetBermasalah(
    request=None,
    id_jlega=None
):

    qs = AsetKelompok.objects.exclude(
        kondisi='baik'
    )

    if id_jlega:
        qs = qs.filter(
            kelompok__jenisKelompok__iexact=id_jlega
        )

    if request:

        wilayah = getWilaya(request)

        if wilayah:
            qs = qs.filter(
                Q(
                    kelompok__desa_id__in=wilayah["desa_ids"]
                ) |
                Q(
                    kelompok_id__in=wilayah["kelompok_ids"]
                )
            ).distinct()

    return qs.select_related(
        'kelompok',
        'kelompok__desa'
    )





def summaryLegalitas(
    request,
    id_jlega='BUMDES'
):

    kelompok = Kelompok.objects.all()

    if request:
        wilayah = getWilaya(request)

        if wilayah:
            kelompok = kelompok.filter(
                    Q(
                        desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()    
    total_kelompok = (
        kelompok
        .filter(
            jenisKelompok__iexact=id_jlega
        )
        .distinct()
        .count()
    )

    total_item = (
        ItemLegalitas.objects
        .filter(
            idJLega=id_jlega
        )
        .count()
    )

    kelompok = (
        kelompok
        .filter(
            jenisKelompok__iexact=id_jlega
        )
        .annotate(
            total_legalitas=Count(
                'legalitaskelompok',
                filter=Q(
                    legalitaskelompok__itemLegalitas__idJLega=id_jlega
                ),
                distinct=True
            )
        )
    )

    lengkap = kelompok.filter(
        total_legalitas=total_item
    ).count()

    return {
        'kelompok': total_kelompok,
        'dokumen': total_item,
        'lengkap': lengkap,
        'kurang': total_kelompok - lengkap,
    }


def chartKelengkapan(
        request,
        id_jlega='BUMDES'
    ):

    summary = summaryLegalitas(
        request,
        id_jlega
    )

    return {
        'lengkap': summary['lengkap'],
        'kurang': summary['kurang']
    }


def chartApproval(
    request=None,
    id_jlega=None
):

    qs = LegalitasKelompok.objects.all()

    if id_jlega:
        qs = qs.filter(
            itemLegalitas__idJLega__iexact=id_jlega
        )

    if request: 
        wilayah = getWilaya(request)

        if wilayah:
            qs = qs.filter(
                    Q(
                        kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()    

    return {
        'pengawal_true': qs.filter(
            aprovalPengawal=True
        ).count(),

        'pengawal_false': qs.filter(
            aprovalPengawal=False
        ).count(),

        'desa_true': qs.filter(
            aprovalDesa=True
        ).count(),

        'desa_false': qs.filter(
            aprovalDesa=False
        ).count(),

        'kecamatan_true': qs.filter(
            aprovalKec=True
        ).count(),

        'kecamatan_false': qs.filter(
            aprovalKec=False
        ).count(),
    }




def chartDokumen(
        request=None,
        id_jlega=None
    ):

    qs = LegalitasKelompok.objects.all()

    if id_jlega:
        qs = qs.filter(
            itemLegalitas__idJLega__iexact=id_jlega
        )

    if request:
        wilayah = getWilaya(request)

        if wilayah:
            qs = qs.filter(
                    Q(
                        kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()    

    return (
        qs.values(
            'itemLegalitas__nmILega'
        )
        .annotate(
            total=Count('id')
        )
        .order_by('-total')
    )


def chartKelompokKurang(
        request=None,
        id_jlega=None
    ):

    qs = Kelompok.objects.all()

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

    if not id_jlega:

        return (
            qs.annotate(
                total_legalitas=Count(
                    'legalitaskelompok',
                    distinct=True
                )
            )
            .values(
                'nmKelo',
                'total_legalitas'
            )
            .order_by('total_legalitas')
        )

    total_item = (
        ItemLegalitas.objects
        .filter(
            idJLega__iexact=id_jlega
        )
        .count()
    )

    return (
        qs.filter(
            jenisKelompok__iexact=id_jlega
        )
        .annotate(
            total_legalitas=Count(
                'legalitaskelompok',
                filter=Q(
                    legalitaskelompok__itemLegalitas__idJLega__iexact=id_jlega
                ),
                distinct=True
            )
        )
        .filter(
            total_legalitas__lt=total_item
        )
        .values(
            'nmKelo',
            'total_legalitas'
        )
        .order_by(
            'total_legalitas',
            'nmKelo'
        )
    )

def tableLegalitas(id_jlega='BUMDES'):

    return (
        LegalitasKelompok.objects
        .select_related(
            'kelompok',
            'itemLegalitas'
        )
        .filter(
            itemLegalitas__idJLega=id_jlega
        )
        .order_by(
            'kelompok__nmKelo'
        )
    )



def summaryApproval(
    request=None,
    id_jlega=None
):

    kelompok_qs = Kelompok.objects.all()

    if request:

        wilayah = getWilaya(request)

        if wilayah:
            kelompok_qs = kelompok_qs.filter(
                Q(
                    desa_id__in=wilayah["desa_ids"]
                ) |
                Q(
                    id__in=wilayah["kelompok_ids"]
                )
            ).distinct()

    kelompok_ids = kelompok_qs.values_list(
        'id',
        flat=True
    )

    legalitas = LegalitasKelompok.objects.filter(
        kelompok_id__in=kelompok_ids
    )

    pendapatan = Pendapatan.objects.filter(
        usaha__kelompok_id__in=kelompok_ids
    )

    if id_jlega:

        legalitas = legalitas.filter(
            itemLegalitas__idJLega__iexact=id_jlega
        )

        pendapatan = pendapatan.filter(
            usaha__kelompok__jenisKelompok__iexact=id_jlega
        )

    total = (
        legalitas.count() +
        pendapatan.count()
    )

    approve = (
        legalitas.filter(
            aprovalKec=True
        ).count()
        +
        pendapatan.filter(
            aprovalKec=True
        ).count()
    )

    return {
        "total": total,
        "approve": approve,
        "pending": total - approve,
        "persen": round(
            (approve / total) * 100,
            1
        ) if total else 0
    }



def chartApprovalModul(
    request=None,
    id_jlega=None
):

    kelompok_qs = Kelompok.objects.all()

    if request:

        wilayah = getWilaya(request)

        if wilayah:
            kelompok_qs = kelompok_qs.filter(
                Q(
                    desa_id__in=wilayah["desa_ids"]
                ) |
                Q(
                    id__in=wilayah["kelompok_ids"]
                )
            ).distinct()

    kelompok_ids = kelompok_qs.values_list(
        'id',
        flat=True
    )

    legalitas = LegalitasKelompok.objects.filter(
        kelompok_id__in=kelompok_ids
    )

    umum = Pendapatan.objects.filter(
        usaha__kelompok_id__in=kelompok_ids,
        jenis='UMUM'
    )

    pades = Pendapatan.objects.filter(
        usaha__kelompok_id__in=kelompok_ids,
        jenis='PADES'
    )

    pajak = Pendapatan.objects.filter(
        usaha__kelompok_id__in=kelompok_ids,
        jenis='PAJAK'
    )

    if id_jlega:

        legalitas = legalitas.filter(
            itemLegalitas__idJLega__iexact=id_jlega
        )

        umum = umum.filter(
            usaha__kelompok__jenisKelompok__iexact=id_jlega
        )

        pades = pades.filter(
            usaha__kelompok__jenisKelompok__iexact=id_jlega
        )

        pajak = pajak.filter(
            usaha__kelompok__jenisKelompok__iexact=id_jlega
        )

    return [
        {
            "nama": "Legalitas",
            "approve": legalitas.filter(
                aprovalKec=True
            ).count(),
            "pending": legalitas.filter(
                aprovalKec=False
            ).count()
        },
        {
            "nama": "Pendapatan",
            "approve": umum.filter(
                aprovalKec=True
            ).count(),
            "pending": umum.filter(
                aprovalKec=False
            ).count()
        },
        {
            "nama": "PADes",
            "approve": pades.filter(
                aprovalKec=True
            ).count(),
            "pending": pades.filter(
                aprovalKec=False
            ).count()
        },
        {
            "nama": "Pajak",
            "approve": pajak.filter(
                aprovalKec=True
            ).count(),
            "pending": pajak.filter(
                aprovalKec=False
            ).count()
        }
    ]


def chartApprovalLevel(
    request=None,
    id_jlega=None
):

    legalitas = LegalitasKelompok.objects.all()
    pendapatan = Pendapatan.objects.all()

    if request:

        wilayah = getWilaya(request)

        if wilayah:

            legalitas = legalitas.filter(
                Q(
                    kelompok__desa_id__in=wilayah["desa_ids"]
                ) |
                Q(
                    kelompok_id__in=wilayah["kelompok_ids"]
                )
            ).distinct()

            pendapatan = pendapatan.filter(
                Q(
                    usaha__kelompok__desa_id__in=wilayah["desa_ids"]
                ) |
                Q(
                    usaha__kelompok_id__in=wilayah["kelompok_ids"]
                )
            ).distinct()

    if id_jlega:

        legalitas = legalitas.filter(
            itemLegalitas__idJLega__iexact=id_jlega
        )

        pendapatan = pendapatan.filter(
            usaha__kelompok__jenisKelompok__iexact=id_jlega
        )

    return {
        'pengawal': (
            legalitas.filter(
                aprovalPengawal=True
            ).count()
            +
            pendapatan.filter(
                aprovalPengawal=True
            ).count()
        ),

        'desa': (
            legalitas.filter(
                aprovalDesa=True
            ).count()
            +
            pendapatan.filter(
                aprovalDesa=True
            ).count()
        ),

        'kecamatan': (
            legalitas.filter(
                aprovalKec=True
            ).count()
            +
            pendapatan.filter(
                aprovalKec=True
            ).count()
        )
    }


def chartPendingModul(
    request=None,
    id_jlega=None
):

    legalitas = LegalitasKelompok.objects.filter(
        aprovalKec=False
    )

    pendapatan = Pendapatan.objects.filter(
        jenis='UMUM',
        aprovalKec=False
    )

    pades = Pendapatan.objects.filter(
        jenis='PADES',
        aprovalKec=False
    )

    pajak = Pendapatan.objects.filter(
        jenis='PAJAK',
        aprovalKec=False
    )

    if request:

        wilayah = getWilaya(request)

        if wilayah:

            legalitas = legalitas.filter(
                Q(
                    kelompok__desa_id__in=wilayah["desa_ids"]
                ) |
                Q(
                    kelompok_id__in=wilayah["kelompok_ids"]
                )
            ).distinct()

            pendapatan = pendapatan.filter(
                Q(
                    usaha__kelompok__desa_id__in=wilayah["desa_ids"]
                ) |
                Q(
                    usaha__kelompok_id__in=wilayah["kelompok_ids"]
                )
            ).distinct()

            pades = pades.filter(
                Q(
                    usaha__kelompok__desa_id__in=wilayah["desa_ids"]
                ) |
                Q(
                    usaha__kelompok_id__in=wilayah["kelompok_ids"]
                )
            ).distinct()

            pajak = pajak.filter(
                Q(
                    usaha__kelompok__desa_id__in=wilayah["desa_ids"]
                ) |
                Q(
                    usaha__kelompok_id__in=wilayah["kelompok_ids"]
                )
            ).distinct()

    if id_jlega:

        legalitas = legalitas.filter(
            itemLegalitas__idJLega__iexact=id_jlega
        )

        pendapatan = pendapatan.filter(
            usaha__kelompok__jenisKelompok__iexact=id_jlega
        )

        pades = pades.filter(
            usaha__kelompok__jenisKelompok__iexact=id_jlega
        )

        pajak = pajak.filter(
            usaha__kelompok__jenisKelompok__iexact=id_jlega
        )

    return {
        'legalitas': legalitas.count(),
        'pendapatan': pendapatan.count(),
        'pades': pades.count(),
        'pajak': pajak.count(),
    }


def chartKelompokPending(
    request=None,
    id_jlega=None
):

    qs = Kelompok.objects.all()

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

    if id_jlega:
        qs = qs.filter(
            jenisKelompok__iexact=id_jlega
        )

    return (
        qs.annotate(
            pending_legalitas=Count(
                'legalitaskelompok',
                filter=Q(
                    legalitaskelompok__aprovalKec=False
                )
            )
        )
        .filter(
            pending_legalitas__gt=0
        )
        .values(
            'nmKelo',
            'pending_legalitas'
        )
        .order_by(
            '-pending_legalitas',
            'nmKelo'
        )[:10]
    )



def summaryDashboard(request=None):
    
    kelompok_qss = Kelompok.objects.all()
    dusaha = ListUsaha.objects.all()
    danggota = AnggotaKelompok.objects.all()
    daset = AsetKelompok.objects.all()

    kelompok_qs =[]
    if request: 
        kelompok_qs = getWilaya(request) 
        if(kelompok_qs):
            kelompok_qss = kelompok_qss.filter(
                Q(
                    desa_id__in=kelompok_qs["desa_ids"]
                ) |
                Q(
                    id__in=kelompok_qs["kelompok_ids"]
                )
            ).distinct()

            dusaha = dusaha.filter(
                Q(
                    kelompok__desa_id__in=kelompok_qs["desa_ids"]
                ) |
                Q(
                    kelompok_id__in=kelompok_qs["kelompok_ids"]
                )
            ).distinct()
            danggota = danggota.filter(
                Q(
                    kelompok__desa_id__in=kelompok_qs["desa_ids"]
                ) |
                Q(
                    kelompok_id__in=kelompok_qs["kelompok_ids"]
                )
            ).distinct()
            daset = daset.filter(
                Q(
                    kelompok__desa_id__in=kelompok_qs["desa_ids"]
                ) |
                Q(
                    kelompok_id__in=kelompok_qs["kelompok_ids"]
                )
            ).distinct()
 

    return {
        'kecamatan': Kecamatan.objects.count(),

        'desa': kelompok_qss.values(
            'desa_id'
        ).distinct().count(),

        'kelompok': kelompok_qss.count(),

        'usaha': dusaha.count(),

        'anggota': danggota.count(),

        'aset': daset.count(),
    }



def summaryAnggota(request):

    qs = AnggotaKelompok.objects.all()

    if request: 
        wilayah = getWilaya(request)

        if wilayah:
            qs = qs.filter(
                    Q(
                        kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()    
    return qs.count()

def warningApproval(request):
    legalitas = LegalitasKelompok.objects.all()

    pendapatan = Pendapatan.objects.all()
    if request: 
        wilayah = getWilaya(request)

        if wilayah:
            legalitas = legalitas.filter(
                    Q(
                        kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()    
            pendapatan = pendapatan.filter(
                    Q(
                        usaha__kelompok__desa_id__in=wilayah["desa_ids"]
                    ) |
                    Q(
                        usaha__kelompok__id__in=wilayah["kelompok_ids"]
                    )
                ).distinct()    
     
    return {
        'legalitas': legalitas.filter(
            aprovalKec=False
        ).count(),

        'pendapatan': pendapatan.filter(
            jenis='UMUM',
            aprovalKec=False
        ).count(),

        'pades': pendapatan.filter(
            jenis='PADES',
            aprovalKec=False
        ).count(),

        'pajak': pendapatan.filter(
            jenis='PAJAK',
            aprovalKec=False
        ).count()
    }





def chartLembaga(request):

    qs = Kelompok.objects.all()

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
 
    return (
        qs.values(
            itemLegalitas__idJLega=F(
                'jenisKelompok'
            )
        )
        .annotate(
            total=Count('id')
        )
        .order_by('-total')
    )

