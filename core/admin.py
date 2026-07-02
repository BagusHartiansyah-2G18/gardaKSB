from django.contrib import admin
from django.urls import reverse
from django.shortcuts import render,redirect
from django.utils.html import format_html

from core.apps.wilayah.models import Kecamatan, Desa
from core.apps.legalitas.models import ItemLegalitas 
from core.apps.keuangan.models import Pendapatan 
from core.apps.kelompok.models import Kelompok, LegalitasKelompok,AnggotaKelompok,AsetKelompok,WilayahPengawas
from core.apps.usaha.models import JenisUsaha, ListUsaha

from itertools import groupby
from django import forms



# admin.site.register(Kecamatan)
# admin.site.register(Desa)
# admin.site.register(ItemLegalitas)
# admin.site.register(JenisUsaha)
# admin.site.register(Kelompok)
# admin.site.register(ListUsaha)
# admin.site.register(LegalitasKelompok)
# admin.site.register(Pendapatan)
# admin.site.register(WilayahPengawas)
# admin.site.register(User)


# ✅ KECAMATAN
@admin.register(Kecamatan)
class KecamatanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nmKec','btnEdit')
    search_fields = ('nmKec',)    
    def btnEdit(self, obj):
        url = reverse('admin:core_kecamatan_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="background:#3b82f6;color:white;padding:4px 10px;border-radius:6px;">Edit</a>',
            url
        )
    btnEdit.short_description = 'Aksi'

   




# ✅ DESA
@admin.register(Desa)
class DesaAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'nmDesa', 'nama_kecamatan','btnEdit')
    search_fields = ('nmDesa', 'kecamatan__nmKec')
    list_filter = ('kecamatan__nmKec',)

    def nama_kecamatan(self, obj):
        return obj.kecamatan.nmKec
    
    nama_kecamatan.short_description = 'Kecamatan'

    def btnEdit(self, obj):
        url = reverse('admin:core_desa_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="background:#3b82f6;color:white;padding:4px 10px;border-radius:6px;">Edit</a>',
            url
        )
    btnEdit.short_description = 'Aksi'



# ✅ ITEM LEGALITAS
@admin.register(ItemLegalitas)
class ItemLegalitasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nmILega','idJLega','btnEdit')
    search_fields = ('nmILega',)
    list_filter = ('idJLega',)
    def btnEdit(self, obj):
        url = reverse('admin:core_itemlegalitas_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="background:#3b82f6;color:white;padding:4px 10px;border-radius:6px;">Edit</a>',
            url
        )
    btnEdit.short_description = 'Aksi'


# ✅ JENIS USAHA
@admin.register(JenisUsaha)
class JenisUsahaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nmJUsaha','btnEdit')
    search_fields = ('nmJUsaha',)
    def btnEdit(self, obj):
        url = reverse('admin:core_jenisusaha_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="background:#3b82f6;color:white;padding:4px 10px;border-radius:6px;">Edit</a>',
            url
        )
    btnEdit.short_description = 'Aksi'


# ✅ KELOMPOK
@admin.register(Kelompok)

class KelompokAdmin(admin.ModelAdmin):
    list_display = ('id', 'nmKelo', 'nama_desa','ketua','btnEdit')
    search_fields = ('nmKelo', 'ketua', 'desa__nmDesa', 'desa__kecamatan__nmKec')
    list_filter = ('kelas','desa__nmDesa', 'desa__kecamatan__nmKec')
    list_select_related = ('desa', 'desa__kecamatan')

    def nama_desa(self, obj):
        return obj.desa.nmDesa
    nama_desa.short_description = 'Desa'

    def nama_kecamatan(self, obj):
        return obj.desa.kecamatan.nmKec
    nama_kecamatan.short_description = 'Kecamatan'

    def btnEdit(self, obj):
        url = reverse('admin:core_kelompok_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="background:#3b82f6;color:white;padding:4px 10px;border-radius:6px;">Edit</a>',
            url
        )
    btnEdit.short_description = 'Aksi'



# ✅ LIST USAHA
@admin.register(ListUsaha)
class ListUsahaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_kelompok', 'nama_jenisUsaha', 'komoditi','btnEdit')
    search_fields = ('kelompok__nmKelo', 'komoditi')
    list_filter = ('jenisUsaha__nmJUsaha','komoditi','status')
    def nama_kelompok(self, obj):
        return obj.kelompok.nmKelo
    def nama_jenisUsaha(self, obj):
        return obj.jenisUsaha.nmJUsaha

    def btnEdit(self, obj):
        url = reverse('admin:core_listusaha_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="background:#3b82f6;color:white;padding:4px 10px;border-radius:6px;">Edit</a>',
            url
        )
    btnEdit.short_description = 'Aksi'


class LegalitasKelompokForm(forms.ModelForm):

    class Meta:
        model = LegalitasKelompok
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        queryset = ItemLegalitas.objects.order_by(
            'idJLega',
            'nmILega'
        )

        choices = []

        for id_jlega, items in groupby(
            queryset,
            lambda x: x.idJLega
        ):

            choices.append((
                id_jlega,
                [
                    (item.id, item.nmILega)
                    for item in items
                ]
            ))

        self.fields['itemLegalitas'].choices = choices


# ✅ LEGALITAS KELOMPOK
@admin.register(LegalitasKelompok)
class LegalitasKelompokAdmin(admin.ModelAdmin):

    form = LegalitasKelompokForm

    list_display = (
        'id',
        'nama_kelompok',
        'jenis_legalitas',
        'nama_itemLegalitas',
        'value', 
    )

    search_fields = (
        'kelompok__nmKelo',
        'value'
    )

    list_filter = (
        'itemLegalitas__idJLega',
        'itemLegalitas__nmILega',
        'aprovalPengawal',
        'aprovalDesa',
        'aprovalKec'
    )

    def nama_kelompok(self, obj):
        return obj.kelompok.nmKelo

    nama_kelompok.short_description = 'Kelompok'

    def jenis_legalitas(self, obj):
        return obj.itemLegalitas.idJLega

    jenis_legalitas.short_description = 'Jenis'

    def nama_itemLegalitas(self, obj):
        return obj.itemLegalitas.nmILega

    nama_itemLegalitas.short_description = 'Item Legalitas'


# ✅ PENDAPATAN
@admin.register(Pendapatan)
class PendapatanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_usaha','nama_komoditi', 'nama_kelompok', 'pendapatan', 'pengeluaran')
    search_fields = ('usaha__kelompok__nmKelo',)
    list_filter = ('dateCreate', 'usaha__jenisUsaha__nmJUsaha', 'usaha__komoditi')

    def nama_kelompok(self, obj):
        return obj.usaha.kelompok.nmKelo
    def nama_usaha(self, obj):
        return obj.usaha.jenisUsaha.nmJUsaha
    def nama_komoditi(self, obj):
        return obj.usaha.komoditi
    


# ✅ WILAYAH PENGAWAS
# @admin.register(WilayahPengawas)
# class WilayahPengawasAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'desa')
#     search_fields = ('user__username', 'desa__nmDesa')
#     list_filter = ('desa',) 

class WilayahPengawasForm(forms.ModelForm):

    class Meta:
        model = WilayahPengawas
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["desa"].queryset = Desa.objects.filter(
            kelompok__isnull=False
        ).distinct()

@admin.register(WilayahPengawas)
class WilayahPengawasAdmin(admin.ModelAdmin):
    form = WilayahPengawasForm
    
    list_display = (
        "user",
        "desa",
        "get_kelompok",
    )   
    
    list_filter = (
        "user", 
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "desa__nmDesa",
        "kelompok__nmKelo",
    )

    
    def get_kelompok(self, obj):
        return obj.kelompok.nmKelo if obj.kelompok else "-"

    get_kelompok.short_description = "Kelompok"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "kelompok":

            desa_id = request.GET.get("desa")

            if desa_id:
                kwargs["queryset"] = Kelompok.objects.filter(
                    desa_id=desa_id
                )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )

@admin.register(AnggotaKelompok)
class AnggotaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kelompok', 'jabatan')
    search_fields = ('nama', 'kelompok__nmKelo')
    list_filter = ('jabatan',)


@admin.register(AsetKelompok)
class AsetAdmin(admin.ModelAdmin):
    list_display = ('namaAset', 'kelompok', 'jumlah', 'kondisi')
    search_fields = ('namaAset',)
    list_filter = ('kondisi',)
