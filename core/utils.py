
from core.apps.kelompok.models import WilayahPengawas

from django.db.models import Sum,Count,Q
from django.db.models.functions import ExtractMonth
from core.apps.kelompok.models import Kelompok,LegalitasKelompok,AnggotaKelompok,AsetKelompok
from core.apps.wilayah.models import Kecamatan, Desa 
from core.apps.usaha.models import ListUsaha

from core.apps.keuangan.models import Pendapatan 
from core.apps.legalitas.models import ItemLegalitas

def subMenu():
    return ( ItemLegalitas.objects
        .values('idJLega')
        .distinct())
def getWilaya(request):
    user = request.user

    if user.is_superuser:
        return None  # ✅ artinya semua akses

    return WilayahPengawas.objects.filter(
        user=user
    ).values_list('desa_id', flat=True).distinct()

def isakses(request):
    user = request.user
    if user.is_superuser:
        return None
    elif user.is_staff:
        return True
    return False

def getFilter(jenis=None, kelompok_id=None, id_jlega=None):
    filters = {}

    if jenis:
        filters['jenis'] = jenis

    if kelompok_id:
        filters['usaha__kelompok_id'] = kelompok_id

    if id_jlega:
        filters[
            'usaha__kelompok__legalitaskelompok__itemLegalitas__idJLega'
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

def chartPendBulanan(jenis=None, kelompok_id=None, id_jlega=None):

    filters = getFilter(
        jenis,
        kelompok_id,
        id_jlega
    )

    data = (
        Pendapatan.objects
        .filter(**filters)
        .annotate(month=ExtractMonth("dateCreate"))
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

def chartPendAll(jenis=None, kelompok_id=None, id_jlega=None):
    
    filters =getFilter(jenis,kelompok_id,id_jlega)
    qs = Pendapatan.objects.filter(**filters)

    return qs.aggregate(
        total_pendapatan=Sum('pendapatan'),
        total_pengeluaran=Sum('pengeluaran'),
        total_laba=Sum('laba')
    )

def chartPendJUsaha(jenis=None, kelompok_id=None, id_jlega=None):
    filters =getFilter(jenis,kelompok_id,id_jlega)
    return (
        Pendapatan.objects
        .filter(**filters)
        .values(
            'usaha__jenisUsaha__nmJUsaha'
        )
        .annotate(
            total=Sum('pendapatan')
        )
        .order_by('-total')
    )

def chartKelompok(id_jlega=None):

    filters = getFilter(None,None,id_jlega)
    return (
        Pendapatan.objects
        .filter(**filters)
        .values(
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

def summaryAset(id_jlega='BUMDES'):

    qs = AsetKelompok.objects.filter(
        kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
    )

    return {
        'total_aset': qs.count(),
        'nilai_aset': qs.aggregate(
            total=Sum('nilai')
        )['total'] or 0,

        'baik': qs.filter(
            kondisi='baik'
        ).count(),

        'rusak': qs.filter(
            kondisi='rusak'
        ).count(),
    }
def chartKondisiAset(id_jlega='BUMDES'):

    qs = AsetKelompok.objects.filter(
        kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
    )

    return {
        'baik': qs.filter(kondisi='baik').count(),
        'perlu': qs.filter(
            kondisi='perlu_perbaikan'
        ).count(),
        'rusak': qs.filter(
            kondisi='rusak'
        ).count()
    }

def chartKategoriAset(id_jlega='BUMDES'):

    return (
        AsetKelompok.objects
        .filter(
            kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
        )
        .values('kategori')
        .annotate(
            total=Count('id')
        )
        .order_by('-total')
    )


def chartAsetKelompok(id_jlega='BUMDES'):

    return (
        AsetKelompok.objects
        .filter(
            kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
        )
        .values(
            'kelompok__nmKelo'
        )
        .annotate(
            total=Sum('nilai')
        )
        .order_by('-total')
    )

def chartAsetBermasalah(id_jlega='BUMDES'):

    return (
        AsetKelompok.objects
        .filter(
            kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
        )
        .exclude(
            kondisi='baik'
        )
        .select_related(
            'kelompok'
        )
    )



def summaryLegalitas(id_jlega='BUMDES'):

    total_kelompok = (
        Kelompok.objects
        .filter(
            legalitaskelompok__itemLegalitas__idJLega=id_jlega
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
        Kelompok.objects
        .annotate(
            total_legalitas=Count(
                'legalitaskelompok',
                filter=Q(
                    legalitaskelompok__itemLegalitas__idJLega=id_jlega
                )
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

def chartKelengkapan(id_jlega='BUMDES'):

    summary = summaryLegalitas(id_jlega)

    return {
        'lengkap': summary['lengkap'],
        'kurang': summary['kurang']
    }

def chartApproval(id_jlega='BUMDES'):

    qs = LegalitasKelompok.objects.filter(
        itemLegalitas__idJLega=id_jlega
    )

    total = qs.count()

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


def chartDokumen(id_jlega='BUMDES'):

    return (
        LegalitasKelompok.objects
        .filter(
            itemLegalitas__idJLega=id_jlega
        )
        .values(
            'itemLegalitas__nmILega'
        )
        .annotate(
            total=Count('id')
        )
        .order_by('-total')
    )
def chartKelompokKurang(id_jlega='BUMDES'):

    total_item = ItemLegalitas.objects.filter(
        idJLega=id_jlega
    ).count()

    return (
        Kelompok.objects
        .annotate(
            total_legalitas=Count(
                'legalitaskelompok',
                filter=Q(
                    legalitaskelompok__itemLegalitas__idJLega=id_jlega
                )
            )
        )
        .filter(
            total_legalitas__lt=total_item
        )
        .values(
            'nmKelo',
            'total_legalitas'
        )
        .order_by('total_legalitas')
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

def summaryApproval(id_jlega=None):

    legalitas = LegalitasKelompok.objects.all()

    pendapatan = Pendapatan.objects.all()

    if id_jlega:
        legalitas = legalitas.filter(
            itemLegalitas__idJLega=id_jlega
        )

        pendapatan = pendapatan.filter(
            usaha__kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
        )

    total = (
        legalitas.count() +
        pendapatan.count()
    )

    approve = (
        legalitas.filter(aprovalKec=True).count() +
        pendapatan.filter(aprovalKec=True).count()
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
def chartApprovalModul(id_jlega=None):

    legalitas = LegalitasKelompok.objects.all()

    umum = Pendapatan.objects.filter(
        jenis='UMUM'
    )

    pades = Pendapatan.objects.filter(
        jenis='PADES'
    )

    pajak = Pendapatan.objects.filter(
        jenis='PAJAK'
    )

    if id_jlega:

        legalitas = legalitas.filter(
            itemLegalitas__idJLega=id_jlega
        )

        umum = umum.filter(
            usaha__kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
        )

        pades = pades.filter(
            usaha__kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
        )

        pajak = pajak.filter(
            usaha__kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
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
def chartApprovalLevel(id_jlega):

    legalitas = LegalitasKelompok.objects.filter(
        itemLegalitas__idJLega=id_jlega
    )

    pendapatan = Pendapatan.objects.filter(
        usaha__kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
    )

    return {
        'pengawal': (
            legalitas.filter(aprovalPengawal=True).count()
            +
            pendapatan.filter(aprovalPengawal=True).count()
        ),

        'desa': (
            legalitas.filter(aprovalDesa=True).count()
            +
            pendapatan.filter(aprovalDesa=True).count()
        ),

        'kecamatan': (
            legalitas.filter(aprovalKec=True).count()
            +
            pendapatan.filter(aprovalKec=True).count()
        )
    }
def chartPendingModul(id_jlega):

    return {
        'legalitas':
            LegalitasKelompok.objects.filter(
                itemLegalitas__idJLega=id_jlega,
                aprovalKec=False
            ).count(),

        'pendapatan':
            Pendapatan.objects.filter(
                jenis='UMUM',
                aprovalKec=False,
                usaha__kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
            ).count(),

        'pades':
            Pendapatan.objects.filter(
                jenis='PADES',
                aprovalKec=False,
                usaha__kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
            ).count(),

        'pajak':
            Pendapatan.objects.filter(
                jenis='PAJAK',
                aprovalKec=False,
                usaha__kelompok__legalitaskelompok__itemLegalitas__idJLega=id_jlega
            ).count()
    } 
def chartKelompokPending(id_jlega):

    return (
        Kelompok.objects
        .filter(
            legalitaskelompok__itemLegalitas__idJLega=id_jlega
        )
        .annotate(
            pending_legalitas=Count(
                'legalitaskelompok',
                filter=Q(
                    legalitaskelompok__aprovalKec=False
                )
            )
        )
        .values(
            'nmKelo',
            'pending_legalitas'
        )
        .order_by('-pending_legalitas')[:10]
    )


def summaryDashboard():

    return {
        'kecamatan': Kecamatan.objects.count(),

        'desa': Desa.objects.count(),

        'kelompok': Kelompok.objects.count(),

        'usaha': ListUsaha.objects.count(),

        'anggota': AnggotaKelompok.objects.count(),

        'aset': AsetKelompok.objects.count(),
    }

def summaryAnggota():
    return AnggotaKelompok.objects.count()

def warningApproval():

    return {
        'legalitas': LegalitasKelompok.objects.filter(
            aprovalKec=False
        ).count(),

        'pendapatan': Pendapatan.objects.filter(
            jenis='UMUM',
            aprovalKec=False
        ).count(),

        'pades': Pendapatan.objects.filter(
            jenis='PADES',
            aprovalKec=False
        ).count(),

        'pajak': Pendapatan.objects.filter(
            jenis='PAJAK',
            aprovalKec=False
        ).count()
    }

def chartLembaga():

    return (
        LegalitasKelompok.objects
        .values(
            'itemLegalitas__idJLega'
        )
        .annotate(
            total=Count('kelompok', distinct=True)
        )
        .order_by('-total')
    )