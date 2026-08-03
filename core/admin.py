from django.contrib import admin
from unfold.admin import ModelAdmin 
from django.urls import reverse
from django.shortcuts import render,redirect
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin

from core.apps.accounts.models import UserProfile
from core.apps.accounts.User.models import User

from core.apps.aktivitas.models import AktivitasPegawai

from core.apps.informasi.models import Notifikasi
from core.apps.informasi.DeviceToken.models import DeviceToken
from core.apps.informasi.MateriBerita.models import MateriBerita

from core.apps.master.models import Kecamatan
from core.apps.master.Bidang.models import Bidang
from core.apps.master.Desa.models import Desa
from core.apps.master.Dinas.models import Dinas

from core.apps.organisasi.models import Organisasi
from core.apps.organisasi.AnggotaOrganisasi.models import AnggotaOrganisasi
from core.apps.organisasi.JenisOrganisasi.models import JenisOrganisasi
from core.apps.organisasi.PersyaratanOrganisasi.models import PersyaratanOrganisasi
from core.apps.organisasi.DokumenOrganisasi.models import DokumenOrganisasi


from core.apps.pengaduan.models import Pengaduan
from core.apps.pengaduan.JenisKasus.models import JenisKasus
from core.apps.pengaduan.LampiranPengaduan.models import LampiranPengaduan
from core.apps.pengaduan.PengaduanHistory.models import PengaduanHistory
from core.apps.pengaduan.VerifikasiPengaduan.models import VerifikasiPengaduan




# from core.apps.legalitas.models import ItemLegalitas 
# from core.apps.keuangan.models import Pendapatan 
# from core.apps.kelompok.models import Kelompok, LegalitasKelompok,AnggotaKelompok,AsetKelompok,WilayahPengawas
# from core.apps.usaha.models import JenisUsaha, ListUsaha

from itertools import groupby
from django import forms

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

@admin.register(Kecamatan)
class KecamatanAdmin(ModelAdmin):
    list_display = ("kode", "nama")
    search_fields = ("kode", "nama")


@admin.register(Desa)
class DesaAdmin(ModelAdmin):
    list_display = (
        "kode",
        "nama",
        "kecamatan",
    )

    list_filter = ("kecamatan",)

    search_fields = (
        "kode",
        "nama",
    )

@admin.register(Dinas)
class DinasAdmin(ModelAdmin):
    list_display = (
        "kode",
        "nama", 
        "telepon",
    )

    search_fields = (
        "kode",
        "nama",
    )


@admin.register(Bidang)
class BidangAdmin(ModelAdmin):
    list_display = (
        "kode",
        "nama",
        "dinas", 
    )

    list_filter = (
        "dinas",
    )

    search_fields = (
        "kode",
        "nama",
    )

@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    autocomplete_fields = (
        "user",
        "desa",
        "bidang",
    )
    list_display = (
        "user",
        "get_nik",
        "get_no_hp",
        "desa",
        "bidang",
        "is_verified",
    )

    list_filter = (
        "is_verified",
        "bidang",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__nik",
        "user__no_hp",
    )
    def has_add_permission(self, request):
        print(
            "SUPERUSER:",
            request.user.is_superuser
        )
        return True
    @admin.display(description="NIK")
    def get_nik(self, obj):
        return obj.user.nik

    @admin.display(description="No HP")
    def get_no_hp(self, obj):
        return obj.user.no_hp
 
@admin.register(PersyaratanOrganisasi)
class PersyaratanOrganisasiAdmin(ModelAdmin):

    list_display = (
        "nama",
        "jenis_organisasi",
        "wajib", 
    )

    list_filter = (
        "jenis_organisasi",
        "wajib",  
    )

    search_fields = (
        "nama",
        "jenis_organisasi__nama",
    )
@admin.register(DeviceToken)
class DeviceTokenAdmin(ModelAdmin):

    list_display = (
        "user",
        "platform",
        "is_active",
        "last_used_at",
        "created_at",
    )

    list_filter = (
        "platform",
        "is_active",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "token",
    )

    autocomplete_fields = (
        "user",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

@admin.register(DokumenOrganisasi)
class DokumenOrganisasiAdmin(ModelAdmin):

    list_display = (
        "organisasi",
        "persyaratan",
        "status",
        "verified_by",
        "verified_at",
    )

    list_filter = (
        "status",
        "persyaratan",
    )

    search_fields = (
        "organisasi__nama",
        "persyaratan__nama",
    )


class JenisKasusForm(forms.ModelForm):
    class Meta:
        model = JenisKasus
        fields = "__all__"
        widgets = {
            "warna": forms.TextInput(
                attrs={
                    "type": "color"
                }
            )
        }
 
@admin.register(JenisKasus)
class JenisKasusAdmin(ModelAdmin):
    form = JenisKasusForm
    list_display = (
        "kode",
        "nama",
        "warna_preview",
    )

    search_fields = (
        "kode",
        "nama",
    )

    ordering = (
        "kode",
    )

    list_per_page = 20

    readonly_fields = (
        "warna_preview",
    )

    fields = (
        "kode",
        "nama",
        "warna",
        "warna_preview",
    )

    def warna_preview(self, obj):

        if not obj.warna:
            return "-"

        return format_html(
            '''
            <div style="
                width:40px;
                height:40px;
                border-radius:6px;
                background:{};
                border:1px solid #ddd;
            "></div>
            ''',
            obj.warna
        )

    warna_preview.short_description = "Preview"


@admin.register(JenisOrganisasi)
class JenisOrganisasiAdmin(ModelAdmin):
    list_display = (
        "kode",
        "nama",
    )


class LampiranPengaduanInline(admin.TabularInline):
    model = LampiranPengaduan
    extra = 0


class PengaduanHistoryInline(admin.TabularInline):
    model = PengaduanHistory
    extra = 0


@admin.register(Pengaduan)
class PengaduanAdmin(ModelAdmin):

    list_display = (
        "nomor_tiket",
        "jenis_kasus",
        "pelapor",
        "status",
        "prioritas",
        "verifikasi_admin",
        "created_at",
    )

    list_filter = (
        "status",
        "prioritas",
        "verifikasi_admin",
        "jenis_kasus",
    )

    search_fields = (
        "nomor_tiket",
        "nama_pelapor",
        "hp_pelapor",
        "uraian",
    )

    readonly_fields = (
        "ip_address",
        "user_agent",
        "created_at",
        "updated_at",
    )

    inlines = [
        LampiranPengaduanInline,
        PengaduanHistoryInline,
    ]

@admin.register(PengaduanHistory)
class PengaduanHistoryAdmin(ModelAdmin):

    list_display = (
        "pengaduan",
        "user",
        "judul",
        "status_lama",
        "status_baru",
        "created_at",
    )

    list_filter = (
        "status_baru",
    )

    search_fields = (
        "judul",
        "deskripsi",
    )

@admin.register(VerifikasiPengaduan)
class VerifikasiPengaduanAdmin(ModelAdmin):

    list_display = (
        "pengaduan",
        "user",
        "peran",
        "status_verifikasi",
    )

    list_filter = (
        "peran",
        "status_verifikasi",
    )
class AnggotaOrganisasiInline(admin.TabularInline):
    model = AnggotaOrganisasi
    extra = 0


@admin.register(Organisasi)
class OrganisasiAdmin(ModelAdmin):

    list_display = (
        "nama_organisasi",
        "jenis_organisasi",
        "ketua",
        "desa",
        "status_verifikasi",
    )

    list_filter = (
        "jenis_organisasi",
        "status_verifikasi",
    )

    search_fields = (
        "nama_organisasi",
    )

    inlines = [
        AnggotaOrganisasiInline
    ]


@admin.register(AnggotaOrganisasi)
class AnggotaOrganisasiAdmin(ModelAdmin):

    list_display = (
        "nama",
        "jabatan",
        "organisasi",
        "no_hp",
    )

    search_fields = (
        "nama",
        "nik",
    )

@admin.register(MateriBerita)
class MateriBeritaAdmin(ModelAdmin):

    list_display = (
        "judul",
        "kategori",
        "user",
        "is_public",
        "status_publish",
        "published_at",
    )

    list_filter = (
        "kategori",
        "is_public",
        "status_publish",
    )

    search_fields = (
        "judul",
    )

    prepopulated_fields = {
        "slug": ("judul",)
    }

@admin.register(AktivitasPegawai)
class AktivitasPegawaiAdmin(ModelAdmin):

    list_display = (
        "judul",
        "user",
        "tanggal_aktivitas",
    )

    list_filter = (
        "tanggal_aktivitas",
    )

    search_fields = (
        "judul",
        "deskripsi",
    )
@admin.register(Notifikasi)
class NotifikasiAdmin(ModelAdmin):

    list_display = (
        "judul",
        "user",
        "status_baca",
        "created_at",
    )

    list_filter = (
        "status_baca",
    )

    search_fields = (
        "judul",
        "pesan",
    )