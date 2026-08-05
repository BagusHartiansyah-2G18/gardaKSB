from django.contrib import admin
from unfold.admin import ModelAdmin 
from django.urls import reverse
from django.shortcuts import render,redirect
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin

from core.apps.accounts.models import UserProfile
from core.apps.accounts.User.models import User

from core.apps.aktivitas.models import AktivitasPegawai
from django.urls import path,reverse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils import timezone

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
 

from itertools import groupby
from django import forms
from core.utils import filterByGroup,aksesMenuAdmin,filterData,setKeyGroup
from core.apps.accounts.service import getAllID

from core.viewForm import VerifikasiPengaduanForm

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None:
           
            dataKey = setKeyGroup(
                anggota=idUser,
                kabid=allID.idBidang,
                publik=idUser
            ) 
            groupKey = setKeyGroup(
                anggota="id",
                kabid="userprofile__bidang_id",
                publik="id"
            )
            groupKeys= groupKey.get(groupUser.name)
            qs = filterData(request,qs,groupKey=groupKeys,groupData=dataKey)
        else:
            return qs.none()
        return qs
        
    pass

@admin.register(Kecamatan)
class KecamatanAdmin(ModelAdmin):
    list_display = ("kode", "nama")
    search_fields = ("kode", "nama")
    
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        duser = getUserID(idUser)

        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None: 
            dataKey = setKeyGroup(
                anggota=allID.idKecamatan,
                kabid=allID.idKecamatan,
                publik=allID.idKecamatan
            )
            qs = filterData(request,qs,groupKey="id",groupData=dataKey)
        else:
            return qs.none()
        return qs

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
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None: 
            dataKey = setKeyGroup(
                anggota=allID.idDesa,
                kabid=allID.idDesa,
                publik=allID.idDesa
            )
            qs = filterData(request,qs,groupKey="id",groupData=dataKey)
        else:
            return qs.none()
        return qs

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
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None: 
            dataKey = setKeyGroup(
                anggota=allID.idDinas,
                kabid=allID.idDinas,
                publik=allID.idDinas
            )
            qs = filterData(request,qs,groupKey="id",groupData=dataKey)
        else:
            return qs.none()
        return qs


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
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        allID = getAllID(idUser)
        qs = super().get_queryset(request) 
        if allID != None: 
            dataKey = setKeyGroup(
                anggota=allID.idBidang,
                kabid=allID.idBidang,
                publik=allID.idBidang
            )
            qs = filterData(request,qs,groupKey="id",groupData=dataKey)
        else:
            return qs.none()
        return qs

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
    @admin.display(description="NIK")
    def get_nik(self, obj):
        return obj.user.nik

    @admin.display(description="No HP")
    def get_no_hp(self, obj):
        return obj.user.no_hp
    
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None:
            dataKey = setKeyGroup(
                anggota=idUser,
                kabid=allID.idBidang,
                publik=idUser
            ) 
            groupKey = setKeyGroup(
                anggota="user_id",
                kabid="bidang_id",
                publik="user_id"
            )
            groupKeys= groupKey.get(groupUser.name)
            qs = filterData(request,qs,groupKey=groupKeys,groupData=dataKey)
        else:
            return qs.none()
        return qs
 
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
    # def get_queryset(self, request):

    #     idUser = request.user.id
    #     groupUser = request.user.groups.first()

    #     allID = getAllID(idUser)

    #     qs = super().get_queryset(request)
    #     dataKey = setKeyGroup( 
    #         publik=idUser
    #     ) 
    #     groupKey = setKeyGroup( 
    #         publik="organisasi__ketua_id",
    #     )
    #     groupKeys= groupKey.get(groupUser.name)
    #     qs = filterData(request,qs,groupKey=groupKeys,groupData=dataKey)
    #     else:
    #   return qs


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
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None: 
            dataKey = setKeyGroup( 
                publik=idUser
            ) 
            groupKey = setKeyGroup( 
                publik="organisasi__ketua_id",
            )
            groupKeys= groupKey.get(groupUser.name)
            qs = filterData(request,qs,groupKey=groupKeys,groupData=dataKey)
        else:
            return qs.none()
        return qs



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
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None: 
            dataKey = setKeyGroup(
                anggota=allID.idBidang,
                kabid=allID.idBidang,
                publik=idUser
            )  

            groupKey = setKeyGroup( 
                anggota="pengaduan__bidang_disposisi_id",
                kabid="pengaduan__bidang_disposisi_id",
                publik="user_id",
            )
            groupKeys= groupKey.get(groupUser.name)
            qs = filterData(request,qs,groupKey=groupKeys,groupData=dataKey)
        else:
            return qs.none()
        return qs

class PengaduanHistoryInline(admin.TabularInline):
    model = PengaduanHistory
    extra = 0
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None: 
            dataKey = setKeyGroup(
                anggota=allID.idBidang,
                kabid=allID.idBidang,
                publik=idUser
            )  

            groupKey = setKeyGroup( 
                anggota="bidang_id",
                kabid="bidang_id",
                publik="user_id",
            )
            groupKeys= groupKey.get(groupUser.name)
            qs = filterData(request,qs,groupKey=groupKeys,groupData=dataKey)
        else:
            return qs.none()
        return qs


@admin.register(Pengaduan)
class PengaduanAdmin(ModelAdmin):

    list_display = (
        "nomor_tiket",
        "nama_pelapor",
        "status",
        "prioritas",
        "verifikasi_admin",
        "created_at",
        "aksi",
    )

    list_filter = (
        "status",
        "prioritas",
        "verifikasi_admin",
    )

    search_fields = (
        "nomor_tiket",
        "nama_pelapor",
        "judul",
        "uraian",
    )

    ordering = (
        "-created_at",
    )

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [
            path(
                "verifikasi/<int:pk>/",
                self.admin_site.admin_view(
                    self.verifikasi_view
                ),
                name="verifikasi_pengaduan",
            ),
        ]

        return custom_urls + urls

    def aksi(self, obj):
        request = self.request
        detail_url = reverse(
            "admin:pengaduan_pengaduan_change",
            args=[obj.id]
        )

        verifikasi_url = reverse(
            "admin:verifikasi_pengaduan",
            args=[obj.id]
        )

        buttons = []  
        groupUser = request.user.groups.first()
        if (
            request.user.is_superuser
            or (
                groupUser
                and 
                groupUser.name  in ["KABID", "KABAN","ADMIN"]
            )
        ):
            buttons.append(
                f'<a href="{verifikasi_url}" class="bg-green-600 flex h-[38px] items-center justify-center rounded-default shrink-0 text-white text-xs">Verifikasi</a>'
            )

        # buttons.append( 
        #     f'<a href="{detail_url}" class="bg-primary-600 flex h-[38px] items-center justify-center rounded-default shrink-0 text-white text-xs ">Detail</a>'
        # )
        print(buttons)

        return format_html(
            "".join(buttons)
        )
    

    aksi.short_description = "Aksi"

    def verifikasi_view(
        self,
        request,
        pk
    ):

        pengaduan = get_object_or_404(
            Pengaduan,
            pk=pk
        )

        if request.method == "POST":

            form = VerifikasiPengaduanForm(
                request.POST
            )

            if form.is_valid():

                pengaduan.petugas = form.cleaned_data[
                    "petugas"
                ]

                pengaduan.verifikator = (
                    request.user
                )

                pengaduan.verifikasi_admin = True

                pengaduan.status = (
                    "VERIFIKASI"
                )

                pengaduan.verified_at = (
                    timezone.now()
                )

                pengaduan.save()

                return redirect(
                    "/admin/pengaduan/pengaduan/"
                )

        else:

            form = VerifikasiPengaduanForm()

        context = {
            **self.admin_site.each_context(
                request
            ),
            "title": "Verifikasi Pengaduan",
            "form": form,
            "pengaduan": pengaduan,
        }

        return TemplateResponse(
            request,
            "admin/pengaduan/verifikasi.html",
            context,
        )

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        group_user = request.user.groups.first()

        if not group_user:
            return qs.none()

        all_id = getAllID(
            request.user.id
        )

        if not all_id:
            return qs.none()

        data_key = setKeyGroup(
            anggota=all_id.idBidang,
            kabid=all_id.idBidang,
            publik=request.user.id,
        )

        group_key = setKeyGroup(
            anggota="bidang_disposisi_id",
            kabid="bidang_disposisi_id",
            publik="pelapor_id",
        )

        return filterData(
            request,
            qs,
            groupKey=group_key.get(
                group_user.name
            ),
            groupData=data_key,
        )
    

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
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None: 
            dataKey = setKeyGroup( 
                publik=idUser
            ) 
            groupKey = setKeyGroup( 
                publik="organisasi__ketua_id",
            )
            groupKeys= groupKey.get(groupUser.name)
            qs = filterData(request,qs,groupKey=groupKeys,groupData=dataKey)
        else:
            return qs.none()
        return qs

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
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None: 
            dataKey = setKeyGroup(
                anggota=idUser,
                kabid=allID.idBidang,
                publik=idUser
            ) 
            groupKey = setKeyGroup(
                anggota="user_id",
                kabid="user__userprofile__bidang_id",
                kaban="user__userprofile__bidang__dinas_id",
            )
            groupKeys= groupKey.get(groupUser.name)
            qs = filterData(request,qs,groupKey=groupKeys,groupData=dataKey)
        else:
            return qs.none()
        return qs

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
    ordering = [
        "user",
        "id"
    ]
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None: 
            dataKey = setKeyGroup(
                anggota=idUser,
                kabid=allID.idBidang,
                publik=idUser
            ) 
            groupKey = setKeyGroup(
                anggota="user_id",
                kabid="user__userprofile__bidang_id",
                kaban="user__userprofile__bidang__dinas_id",
            )
            groupKeys= groupKey.get(groupUser.name)
            qs = filterData(request,qs,groupKey=groupKeys,groupData=dataKey)
        else:
            return qs.none()
        return qs
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
    def get_queryset(self, request):

        idUser = request.user.id
        groupUser = request.user.groups.first()

        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None: 
            dataKey = setKeyGroup(
                anggota=idUser,
                kabid=allID.idBidang,
                publik=idUser
            ) 
            groupKey = setKeyGroup(
                anggota="user_id",
                kabid="user__userprofile__bidang_id",
                kaban="user__userprofile__bidang__dinas_id",
            )
            groupKeys= groupKey.get(groupUser.name)
            qs = filterData(request,qs,groupKey=groupKeys,groupData=dataKey)
        else:
            return qs.none()
        return qs