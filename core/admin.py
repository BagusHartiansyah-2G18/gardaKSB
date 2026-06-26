from django.contrib import admin
# from .models import Kecamatan

from core.apps.wilayah.models import Kecamatan, Desa, WilayahPengawas
from core.apps.legalitas.models import ItemLegalitas 
from core.apps.keuangan.models import Pendapatan 
from core.apps.kelompok.models import Kelompok
from core.apps.usaha.models import JenisUsaha, ListUsaha




admin.site.register(Kecamatan)
admin.site.register(Desa)
admin.site.register(ItemLegalitas)
admin.site.register(JenisUsaha)
admin.site.register(Kelompok)
admin.site.register(ListUsaha)
# admin.site.register(LegalitasKelompok)
admin.site.register(Pendapatan)
# admin.site.register(User)
admin.site.register(WilayahPengawas)
