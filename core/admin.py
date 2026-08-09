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
from core.apps.accounts.service import getAllID,getUserByID

from django.utils.text import Truncator
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
        "uraian_singkat",
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
    
    @admin.display(description="Uraian")
    def uraian_singkat(self, obj):
        return Truncator(obj.uraian).chars(30) 
     
    def get_exclude(self, request, obj=None):

        # Form Add
        if obj is None:
            return (
                "nomor_tiket",
                "source",
                "ip_address",
                "user_agent",
                "created_at",
                "updated_at",
                "status",
                "prioritas",
                "bidang_disposisi",
                "verifikator",
                "verified_at",
                "disposisi_oleh",
                "disposisi_at",
                "petugas",
                "verifikasi_admin",
                "tindak_lanjut",
                "kesimpulan",
                "nama_pelapor",
                "hp_pelapor",
                "email_pelapor",
                "alamat_pelapor",
                "anonim",
            )

        # Form Edit
        return ()
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

        verifikasi_url = reverse(
            "admin:verifikasi_pengaduan",
            args=[obj.id]
        )
        history_url = (
            reverse(
                "admin:pengaduan_pengaduanhistory_changelist"
            )
            + f"?e={obj.id}"
        )
        
        pageVerifikasi_url = reverse(
            "admin:pengaduan_verifikasipengaduan_changelist"
        )+ f"?e={obj.id}"
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
            if not obj.verifikasi_admin:
                buttons.append(
                    f'<a href="{verifikasi_url}" class="bg-green-600 flex h-[38px] items-center justify-center rounded-default shrink-0 text-white text-xs p-2">Verifikasi</a>'
                )
            else:
                buttons.append(
                    f'<a href="{pageVerifikasi_url}" class="bg-green-600 flex h-[38px] items-center justify-center rounded-default shrink-0 text-white text-xs p-2">tim Verifikasi</a>'
                )


        # if(len(buttons)==0):
        buttons.append( 
            f'<a href="{history_url}" class="bg-blue-400 flex h-[38px] items-center justify-center rounded-default shrink-0 text-black text-xs p-2">riwayat</a>'
        )
        # print(buttons)
        return format_html(
            '''
            <div class="flex items-center gap-2">
                {}
            </div>
            ''',
            format_html("".join(buttons))
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
                pengaduan.disposisi_oleh = (request.user)

                pengaduan.tindak_lanjut = form.cleaned_data[
                    "catatan"
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

            form = VerifikasiPengaduanForm(
                initial={
                    "petugas": pengaduan.petugas,
                    "catatan": getattr(pengaduan, "tindak_lanjut", "")
                }
            )

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

    change_list_template = (
        "admin/pengaduan/pageHistory.html"
    )
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)

        id_pengaduan = request.GET.get("e")
        initial["user"] = request.user.pk
        duser =  getUserByID(request.user.pk) 
        initial["bidang"] = duser.bidang.id if duser.bidang.id else None
        if id_pengaduan:
            initial["pengaduan"] = id_pengaduan

        return initial
    exclude = (
        # "user",
        "bidang",
        "status_lama",
        "status_baru",
        
    )
    # def has_add_permission(self, request):
    #     return False
    def save_model(self, request, obj, form, change):
        if not change:
            # obj.user = request.user
            duser =  getUserByID(obj.user.pk) 
            obj.bidang = duser.bidang if duser.bidang else None

            id_pengaduan = request.GET.get("e")
            if id_pengaduan:
                obj.pengaduan_id = id_pengaduan

        super().save_model(request, obj, form, change)
    def changelist_view(
        self,
        request,
        extra_context=None
    ):

        id_pengaduan = request.GET.get(
            "e"
        )

        pengaduan = None
        if not id_pengaduan:
            return redirect("/admin/pengaduan/pengaduan/")
        if id_pengaduan:
            pengaduan = (
                Pengaduan.objects
                .select_related(
                    "petugas",
                    "verifikator",
                    "pelapor"
                )
                .filter(
                    pk=id_pengaduan
                )
                .first()
            )

        extra_context = (
            extra_context or {}
        )

        extra_context.update({
            "pengaduan": pengaduan
        })

        return super().changelist_view(
            request,
            extra_context=extra_context
        )
    def response_add(
        self,
        request,
        obj,
        post_url_continue=None
    ):

        e = request.GET.get("e")

        if e:
            return redirect(
                f"/admin/pengaduan/pengaduanhistory/?e={e}"
            )

        return super().response_add(
            request,
            obj,
            post_url_continue
        )
    def get_queryset(
        self,
        request
    ):

        qs = super().get_queryset(
            request
        )

        id_pengaduan = request.GET.get(
            "e"
        )

        if id_pengaduan:
            qs = qs.filter(
                pengaduan_id=id_pengaduan
            )

        return qs

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
    change_list_template = (
        "admin/pengaduan/pageVerifikasi.html"
    )
    exclude = (
        # "user",
        "status_verifikasi",
        "catatan",
        "tanggal_verifikasi",
        
    )
    # def has_add_permission(self, request):
    #     return False
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)

        id_pengaduan = request.GET.get("e")
        initial["peran"] = "TIM"
        # duser =  getUserByID(request.user.pk) 
        # initial["bidang"] = duser.bidang.id if duser.bidang.id else None
        if id_pengaduan:
            initial["pengaduan"] = id_pengaduan

        return initial
    def response_add(
        self,
        request,
        obj,
        post_url_continue=None
    ):

        e = request.GET.get("e")

        if e:
            return redirect(
                f"/admin/pengaduan/verifikasipengaduan/?e={e}"
            )

        return super().response_add(
            request,
            obj,
            post_url_continue
        )
    def changelist_view(
        self,
        request,
        extra_context=None
    ):

        id_pengaduan = request.GET.get(
            "e"
        )
    
        pengaduan = None
        if not id_pengaduan:
            return redirect("/admin/pengaduan/pengaduan/")
        if id_pengaduan:
            pengaduan = (
                Pengaduan.objects
                .select_related(
                    "petugas",
                    "verifikator",
                    "pelapor"
                )
                .filter(
                    pk=id_pengaduan
                )
                .first()
            )

        extra_context = (
            extra_context or {}
        )

        extra_context.update({
            "pengaduan": pengaduan,
            # "show_save_and_continue": False,
            # "show_save_and_add_another": False,
            # "show_save": False,
        })

        return super().changelist_view(
            request,
            # object_id,form_url,
            extra_context=extra_context
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