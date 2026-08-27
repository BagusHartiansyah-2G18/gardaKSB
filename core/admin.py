from django.contrib import admin
from httpcore import request
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

from core.apps.pengaduan.service import generateNomorTiket

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
from core.form import UploadDokumenOrganisasiForm,VerifikasiForm
from django.contrib.auth.models import Group
admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "total_user",
    )

    def total_user(self, obj):
        return obj.user_set.count()

    total_user.short_description = "Total User"

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
                masyarakat=idUser
            ) 
            groupKey = setKeyGroup(
                anggota="id",
                kabid="userprofile__bidang_id",
                masyarakat="id"
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
        allID = getAllID(idUser)
        qs = super().get_queryset(request)
        if allID != None: 
            dataKey = setKeyGroup(
                anggota=allID.idKecamatan,
                kabid=allID.idKecamatan,
                masyarakat=allID.idKecamatan
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
                masyarakat=allID.idDesa
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
                masyarakat=allID.idDinas
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
                masyarakat=allID.idBidang
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
                masyarakat=idUser
            ) 
            groupKey = setKeyGroup(
                anggota="user_id",
                kabid="bidang_id",
                masyarakat="user_id"
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
    #         masyarakat=idUser
    #     ) 
    #     groupKey = setKeyGroup( 
    #         masyarakat="organisasi__ketua_id",
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

class DokumenOrganisasiInline(admin.TabularInline):
    model = DokumenOrganisasi
    extra = 0

 
from django.contrib import messages 

@admin.register(DokumenOrganisasi)
class DokumenOrganisasiAdmin(ModelAdmin):

    list_display = (
        "organisasi",
        "persyaratan",
        "status",
        "verified_by",
        "verified_at",
    )

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "upload/",
                self.admin_site.admin_view(
                    self.upload_view
                ),
                name="dokumen_organisasi_upload",
            ),
        ]

        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        return redirect(
            "admin:dokumen_organisasi_upload"
        )

    def upload_view(self, request):

        organisasi = None
        persyaratan_data = []

        if request.method == "POST":
            organisasi_id = request.POST.get("organisasi")
            persyaratan_id = request.POST.get("persyaratan_id")

            organisasi = Organisasi.objects.filter(
                pk=organisasi_id
            ).first()

            if organisasi and persyaratan_id:
                file = request.FILES.get("file")

                if file:
                    persyaratan = PersyaratanOrganisasi.objects.get(
                        pk=persyaratan_id
                    )

                    DokumenOrganisasi.objects.update_or_create(
                        organisasi=organisasi,
                        persyaratan=persyaratan,
                        defaults={
                            "file": file
                        }
                    )

                    messages.success(
                        request,
                        f"Dokumen {persyaratan.nama} berhasil diupload."
                    )

                return redirect(
                    f"{request.path}?organisasi={organisasi.id}"
                )

        organisasi_id = request.GET.get(
            "organisasi"
        )

        if organisasi_id:

            organisasi = Organisasi.objects.filter(
                pk=organisasi_id
            ).first()

            if organisasi:

                persyaratan_list = PersyaratanOrganisasi.objects.filter(
                    jenis_organisasi=organisasi.jenis_organisasi
                )

                dokumen_map = {
                    d.persyaratan_id: d
                    for d in DokumenOrganisasi.objects.filter(
                        organisasi=organisasi
                    )
                }

                for p in persyaratan_list:

                    persyaratan_data.append({
                        "persyaratan": p,
                        "dokumen": dokumen_map.get(p.id)
                    })

        context = {
            **self.admin_site.each_context(request),
            "title": "Upload Dokumen Organisasi",
            "organisasi_list": Organisasi.objects.all().order_by(
                "nama_organisasi"
            ),
            "organisasi": organisasi,
            "persyaratan_data": persyaratan_data,
        }

        return render(
            request,
            "admin/upload_dokumen.html",
            context,
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
        "total_organisasi",
    )
    list_filter = (
        "nama", 
    )
    search_fields = (
        "nama",
    )
    def total_organisasi(self, obj):
        return Organisasi.objects.filter(
            jenis_organisasi=obj
        ).count()

    total_organisasi.short_description = "Total Organisasi"

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
                masyarakat=idUser
            )  

            groupKey = setKeyGroup( 
                anggota="pengaduan__bidang_disposisi_id",
                kabid="pengaduan__bidang_disposisi_id",
                masyarakat="user_id",
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
                masyarakat=idUser
            )  

            groupKey = setKeyGroup( 
                anggota="bidang_id",
                kabid="bidang_id",
                masyarakat="user_id",
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
    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):

        is_new = not change

        if is_new:

            if not obj.nomor_tiket:
                obj.nomor_tiket = (
                    generateNomorTiket()
                )

            if not (
                request.user.is_superuser
                or request.user.groups.filter(
                    name="ADMIN"
                ).exists()
            ):

                obj.pelapor = request.user

                profile = getattr(
                    request.user,
                    "profile",
                    None
                )

                if profile:

                    obj.desa = profile.desa

                obj.nama_pelapor = (
                    request.user.get_full_name()
                    or request.user.username
                )

                obj.hp_pelapor = (
                    request.user.no_hp
                )

                obj.email_pelapor = (
                    request.user.email
                )

        super().save_model(
            request,
            obj,
            form,
            change
        )

        if is_new:

            PengaduanHistory.objects.create(
                pengaduan=obj,
                user=request.user,
                judul="Pengaduan Dibuat",
                deskripsi="Pengaduan berhasil dibuat.",
                status_lama="",
                status_baru="BARU",
                latitude=obj.latitude,
                longitude=obj.longitude,
            )
    @admin.display(description="Uraian")
    def uraian_singkat(self, obj):
        return Truncator(obj.uraian).chars(30) 
     
    def get_exclude(self, request, obj=None):
        exclude = [
            "nomor_tiket",
            "source",
            "ip_address",
            "user_agent",
            "created_at",
            "updated_at",
            "status",
            "bidang_disposisi",
            "verifikator",
            "verified_at",
            "disposisi_oleh",
            "disposisi_at",
            "petugas",
            "verifikasi_admin",
            "tindak_lanjut",
            "kesimpulan",
        ]

        if obj is None:

            if (
                request.user.is_superuser
                or request.user.groups.filter(
                    name="ADMIN"
                ).exists()
            ):

                exclude += [
                    "nama_pelapor",
                    "hp_pelapor",
                    "email_pelapor",
                    "alamat_pelapor",
                    "anonim",
                ]

            else:

                exclude += [
                    "pelapor",
                    "desa",
                    "nama_pelapor",
                    "hp_pelapor",
                    "email_pelapor",
                    "alamat_pelapor",
                    "anonim",
                    "prioritas",
                ]

        return tuple(exclude)

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
                PengaduanHistory.objects.create(
                    pengaduan=pengaduan,
                    user=pengaduan.petugas,
                    judul="Pengaduan Diverifikasi",
                    deskripsi="pengaduan telah dialuhkan ke bidang terkait untuk ditindaklanjuti",
                    status_lama="",
                    status_baru="Diverifikasi",
                    latitude=pengaduan.latitude,
                    longitude=pengaduan.longitude
                )
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
            masyarakat=request.user.id,
        )

        group_key = setKeyGroup(
            anggota="bidang_disposisi_id",
            kabid="bidang_disposisi_id",
            masyarakat="pelapor_id",
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


from django.utils.html import format_html

@admin.register(Organisasi)
class OrganisasiAdmin(ModelAdmin):

    list_display = (
        "nama_organisasi",
        "jenis_organisasi",
        "petugas_display",
        "desa",
        "status_dokumen",
        "status_verifikasi",
    )

    def petugas_display(self, obj):
        return obj.ketua

    petugas_display.short_description = "Petugas"
    petugas_display.admin_order_field = "ketua"
    list_filter = (
        "jenis_organisasi",
        "status_verifikasi",
        "desa",
    )
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(
            db_field,
            request,
            **kwargs
        )

        if db_field.name == "ketua":
            formfield.label = "Petugas"

        return formfield
    search_fields = (
        "nama_organisasi",
        "ketua",
    )
    def get_exclude(self, request, obj=None):
        is_admin_group = request.user.groups.filter(
            name__in=[
                "ADMIN",
                "KABAN",
                "KABID",
                "SEKBAN",
            ]
        ).exists()

        if not (
            request.user.is_superuser
            or is_admin_group
        ):
            return ("petugas",)

        return ()
    inlines = [
        AnggotaOrganisasiInline,
        # DokumenOrganisasiInline
    ]

    def status_dokumen(self, obj):

        total = PersyaratanOrganisasi.objects.filter(
            jenis_organisasi=obj.jenis_organisasi
        ).count()

        uploaded = DokumenOrganisasi.objects.filter(
            organisasi=obj
        ).exclude(
            file=""
        ).count()

        warna = (
            "green"
            if uploaded == total and total > 0
            else "orange"
        )

        return format_html(
            '<b style="color:{};">{}/{}</b>',
            warna,
            uploaded,
            total
        )

    status_dokumen.short_description = "Dokumen"


from django.contrib import admin
from django.db.models.functions import Lower


class JabatanFilter(admin.SimpleListFilter):
    title = "Jabatan"
    parameter_name = "jabatan"

    def lookups(self, request, model_admin):
        data = (
            model_admin.get_queryset(request)
            .annotate(jabatan_lower=Lower("jabatan"))
            .values_list("jabatan_lower", flat=True)
            .distinct()
            .order_by("jabatan_lower")
        )

        return [(j, j.title()) for j in data if j]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                jabatan__iexact=self.value()
            )

        return queryset
@admin.register(AnggotaOrganisasi)
class AnggotaOrganisasiAdmin(ModelAdmin):

    list_display = (
        "nama",
        "jabatan",
        "organisasi",
        "no_hp",
    )
    list_filter = (
        "organisasi", 
        JabatanFilter,
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
                masyarakat=idUser
            ) 
            groupKey = setKeyGroup( 
                masyarakat="organisasi__ketua_id",
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
                masyarakat=idUser
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

# @admin.register(AktivitasPegawai)
# class AktivitasPegawaiAdmin(ModelAdmin):

#     list_display = (
#         "judul",
#         "user",
#         "tanggal_aktivitas",
#     )

#     list_filter = (
#         "tanggal_aktivitas",
#     )
    

#     search_fields = (
#         "judul",
#         "deskripsi",
#     )
#     ordering = [
#         "user",
#         "id"
#     ]
#     def get_queryset(self, request):

#         idUser = request.user.id
#         groupUser = request.user.groups.first()

#         allID = getAllID(idUser)
#         qs = super().get_queryset(request)
#         if allID != None: 
#             dataKey = setKeyGroup(
#                 anggota=idUser,
#                 kabid=allID.idBidang,
#                 masyarakat=idUser
#             ) 
#             groupKey = setKeyGroup(
#                 anggota="user_id",
#                 kabid="user__userprofile__bidang_id",
#                 kaban="user__userprofile__bidang__dinas_id",
#             )
#             groupKeys= groupKey.get(groupUser.name)
#             qs = filterData(request,qs,groupKey=groupKeys,groupData=dataKey)
#         else:
#             return qs.none()
#         return qs
@admin.register(Notifikasi)
class NotifikasiAdmin(ModelAdmin):

    list_display = (
        "judul",
        "user",
        "status_kirim",
        "created_at",
    )

    list_filter = (
        "status_kirim",
         "user",
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
                masyarakat=idUser
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
