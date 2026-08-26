
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.fields.files import FieldFile
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from core.apps.accounts.User.models import User
from core.apps.accounts.models import UserProfile

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
from core.apps.organisasi.DokumenOrganisasi.models import DokumenOrganisasi
from core.apps.organisasi.JenisOrganisasi.models import JenisOrganisasi
from core.apps.organisasi.PersyaratanOrganisasi.models import PersyaratanOrganisasi

from core.apps.pengaduan.models import Pengaduan
from core.apps.pengaduan.JenisKasus.models import JenisKasus
from core.apps.pengaduan.LampiranPengaduan.models import LampiranPengaduan
from core.apps.pengaduan.PengaduanHistory.models import PengaduanHistory
from core.apps.pengaduan.VerifikasiPengaduan.models import VerifikasiPengaduan


from drf_spectacular.utils import extend_schema,OpenApiParameter
from .serializers import *
from django.core.paginator import Paginator

from django.db.models import Q
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
)
from core.apps.pengaduan.service import generateNomorTiket

# ============================================================
# RESPONSE HELPER
# ============================================================

def success_response(
    data=None,
    message="Berhasil.",
    status_code=status.HTTP_200_OK
):
    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
        },
        status=status_code
    )


def error_response(
    message="Terjadi kesalahan.",
    errors=None,
    status_code=status.HTTP_400_BAD_REQUEST
):
    return Response(
        {
            "success": False,
            "message": message,
            "errors": errors or {},
        },
        status=status_code
    )


# ============================================================
# SERIALIZE USER
# ============================================================

def user_data(user):

    group = user.groups.first()

    data = {
        "id": user.id,
        "username": user.username,
        "email": getattr(user, "email", ""),
        "first_name": getattr(user, "first_name", ""),
        "last_name": getattr(user, "last_name", ""),
        "nik": getattr(user, "nik", None),
        "no_hp": getattr(user, "no_hp", None),
        "role": group.name if group else None,
        "is_active": user.is_active,
    }

    return data


# ============================================================
# SERIALIZE MODEL
# ============================================================
 
def serialize_value(value):

    if value is None:
        return None

    if isinstance(value, FieldFile):

        if not value:
            return None

        try:
            return value.url
        except Exception:
            return None

    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            pass

    if hasattr(value, "pk"):
        return value.pk

    return value

def serialize_model(instance):

    data = {}

    for field in instance._meta.fields:

        field_name = field.name

        if field_name == "password":
            continue

        try:
            value = getattr(
                instance,
                field_name
            )

            if isinstance(value, FieldFile):

                if value and value.name:
                    data[field_name] = value.url
                else:
                    data[field_name] = None

            else:

                data[field_name] = serialize_value(
                    value
                )

        except Exception:

            data[field_name] = None

    return data


def filter_by_group(
    request,
    queryset,
    owner_field="pelapor"
):

    user = request.user

    is_admin_group = user.groups.filter(
        name__in=[
            "ADMIN",
            "KABAN",
            "KABID",
            "SEKBAN",
        ]
    ).exists()

    if (
        request.query_params.get("bygroup", "group") == "pribadi"
        or not (user.is_superuser or is_admin_group)
    ):
        queryset = queryset.filter(
            {owner_field: user}
    ) 

    # ====================
    # STATUS
    # ====================

    status_param = request.query_params.get(
        "status"
    )

    if status_param:

        queryset = queryset.filter(
            status=status_param
        )

    # ====================
    # PELAPOR
    # ====================

    pelapor = request.query_params.get(
        "pelapor"
    )
    # print(pelapor)
    if pelapor == "pribadi":

        queryset = queryset.filter(
            pelapor=user
        )

    elif pelapor == "group":

        queryset = queryset.exclude(
            pelapor=user
        )

    # ====================
    # PETUGAS
    # ====================

    petugas = request.query_params.get(
        "petugas"
    )

    if petugas == "pribadi":

        queryset = queryset.filter(
            petugas=user
        )

    elif petugas == "group":

        queryset = queryset.exclude(
            petugas=user
        )

    # ====================
    # VERIFIKATOR
    # ====================

    verifikator = request.query_params.get(
        "verifikator"
    )

    if verifikator == "true":

        queryset = queryset.filter(
            verifikator__isnull=False
        )

    elif verifikator == "false":

        queryset = queryset.filter(
            verifikator__isnull=True
        )

    return queryset


def search_and_paginate(
    request,
    queryset,
    search_fields=None
):

    search = request.query_params.get(
        "search"
    )

    if search and search_fields:

        query = Q()

        for field in search_fields:

            query |= Q(
                **{
                    f"{field}__icontains": search
                }
            )

        queryset = queryset.filter(
            query
        )

    page = int(
        request.query_params.get(
            "page",
            1
        )
    )

    page_size = int(
        request.query_params.get(
            "page_size",
            10
        )
    )

    paginator = Paginator(
        queryset,
        page_size
    )

    page_obj = paginator.get_page(
        page
    )

    return {
        "page": page,
        "page_size": page_size,
        "total_data": paginator.count,
        "total_page": paginator.num_pages,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "results": [
            serialize_model(item)
            for item in page_obj.object_list
        ]
    }

# ============================================================
# AUTH - LOGIN
# ============================================================


class LoginAPIView(APIView):

    permission_classes = [AllowAny]
    
    @extend_schema(
        tags=["Authentication"],
        request=LoginSerializer,
        responses={
            200: LoginResponseSerializer,
        }
    )
    def post(self, request):
        print("LoginAPIView called")
        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        username = serializer.validated_data.get(
            "username"
        )

        password = serializer.validated_data.get(
            "password"
        )

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user is None:

            return error_response(
                "Username atau password salah.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:

            return error_response(
                "Akun tidak aktif.",
                status_code=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(
            user
        )

        return success_response(
            data={
                "access_token": str(
                    refresh.access_token
                ),
                "refresh_token": str(
                    refresh
                ),
                "user": user_data(user)
            },
            message="Login berhasil."
        )


# ============================================================
# AUTH - REFRESH
# ============================================================

class RefreshAPIView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Authentication"],
        request=RefreshTokenSerializer,
        responses=RefreshTokenResponseSerializer,
    )
    def post(self, request):

        serializer = RefreshTokenSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        refresh_token = serializer.validated_data.get(
            "refresh_token"
        )

        try:

            refresh = RefreshToken(
                refresh_token
            )

            return success_response(
                data={
                    "access_token": str(
                        refresh.access_token
                    )
                },
                message="Token berhasil diperbarui."
            )

        except Exception:

            return error_response(
                "Refresh token tidak valid.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

# ============================================================
# AUTH - LOGOUT
# ============================================================

class LogoutAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @extend_schema(
        tags=["Authentication"],
        request=LogoutSerializer,
    )
    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        refresh_token = serializer.validated_data.get(
            "refresh_token"
        )

        if refresh_token:

            try:

                token = RefreshToken(
                    refresh_token
                )

                token.blacklist()

            except Exception:
                pass

        return success_response(
            message="Logout berhasil."
        )

# ============================================================
# AUTH - ME
# ============================================================

class MeAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @extend_schema(
        tags=["Authentication"],
        responses=UserSerializer,
    )
    def get(self, request):

        return success_response(
            data=user_data(
                request.user
            )
        )

# ============================================================
# PROFILE
# ============================================================

class ProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @extend_schema(
        tags=["Profile"],
        responses=UserSerializer,
    )
    def get(self, request):

        data = user_data(
            request.user
        )

        try:

            profile = UserProfile.objects.get(
                user=request.user
            )

            data["profile"] = serialize_model(
                profile
            )

        except UserProfile.DoesNotExist:

            data["profile"] = None

        return success_response(
            data=data
        )

    @extend_schema(
        tags=["Profile"],
        request=ProfileUpdateSerializer,
        responses=UserSerializer,
    )
    @extend_schema(
        tags=["Profile"],
        request=ProfileUpdateSerializer,
    )
    def put(self, request):

        user = request.user

        editable_fields = [
            "first_name",
            "last_name",
            "email",
            "nik",
            "no_hp",
        ]

        for field in editable_fields:

            if field in request.data:

                setattr(
                    user,
                    field,
                    request.data[field]
                )

        user.save()

        return success_response(
            data=user_data(user),
            message="Profile berhasil diperbarui."
        )


# ============================================================
# CHANGE PASSWORD
# ============================================================

class ChangePasswordAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @extend_schema(
        tags=["Authentication"]
    )
    def post(self, request):

        old_password = request.data.get(
            "old_password"
        )

        new_password = request.data.get(
            "new_password"
        )

        confirmation = request.data.get(
            "new_password_confirmation"
        )

        if not old_password:
            return error_response(
                "Password lama wajib diisi."
            )

        if not new_password:
            return error_response(
                "Password baru wajib diisi."
            )

        if new_password != confirmation:
            return error_response(
                "Konfirmasi password tidak sesuai."
            )

        if not request.user.check_password(
            old_password
        ):

            return error_response(
                "Password lama salah."
            )

        request.user.set_password(
            new_password
        )

        request.user.save()

        return success_response(
            message="Password berhasil diubah."
        )


# ============================================================
# DASHBOARD
# ============================================================

class DashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @extend_schema(
        tags=["Dashboard"]
    )
    def get(self, request):

        user = request.user

        group = user.groups.first()

        role = (
            group.name
            if group
            else None
        )

        # ----------------------------------------
        # Pengaduan
        # ----------------------------------------

        if (
            user.is_superuser
            or role == "ADMIN"
        ):

            pengaduan_qs = (
                Pengaduan.objects.all()
            )

        else:

            pengaduan_qs = (
                Pengaduan.objects.filter(
                    pelapor=user
                )
            )

        # ----------------------------------------
        # Aktivitas
        # ----------------------------------------

        aktivitas_qs = (
            AktivitasPegawai.objects.filter(
                user=user
            )
        )

        # ----------------------------------------
        # Notifikasi
        # ----------------------------------------

        notifikasi_qs = (
            Notifikasi.objects.filter(
                user=user
            )
        )

        data = {

            "user": user_data(user),

            "role": role,

            "statistik": {

                "total_pengaduan":
                    pengaduan_qs.count(),

                "pengaduan_baru":
                    pengaduan_qs.filter(
                        status="BARU"
                    ).count(),

                "total_aktivitas":
                    aktivitas_qs.count(),

                "notifikasi_belum_dibaca":
                    notifikasi_qs.filter(
                        status_baca=False
                    ).count(),
            },

            "pengaduan_terbaru": [
                serialize_model(item)
                for item in pengaduan_qs
                .order_by("-created_at")[:5]
            ],

            "aktivitas_terbaru": [
                serialize_model(item)
                for item in aktivitas_qs
                .order_by("-tanggal_aktivitas")[:5]
            ],

            "notifikasi_terbaru": [
                serialize_model(item)
                for item in notifikasi_qs
                .order_by("-created_at")[:5]
            ],
        }

        return success_response(
            data=data
        )


# ============================================================
# AKTIVITAS
# ============================================================

class AktivitasViewSet(
    viewsets.ModelViewSet
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = (
        AktivitasPegawai.objects.all()
    )

    def get_queryset(self):

        user = self.request.user

        if user.is_superuser:

            return AktivitasPegawai.objects.all()

        return AktivitasPegawai.objects.filter(
            user=user
        )

    def list(self, request):

        queryset = self.get_queryset()

        return success_response(
            data=[
                serialize_model(item)
                for item in queryset
                .order_by("-tanggal_aktivitas")
            ]
        )

    def retrieve(
        self,
        request,
        pk=None
    ):

        obj = self.get_object()

        return success_response(
            data=serialize_model(obj)
        )

    def create(
        self,
        request
    ):

        data = request.data.copy()

        data["user"] = request.user.id

        serializer = self._get_serializer(
            data=data
        )

        if not serializer.is_valid():

            return error_response(
                "Data aktivitas tidak valid.",
                serializer.errors
            )

        obj = serializer.save()

        return success_response(
            data=serialize_model(obj),
            message="Aktivitas berhasil ditambahkan.",
            status_code=status.HTTP_201_CREATED
        )

    def _get_serializer(
        self,
        instance=None,
        data=None,
        partial=False
    ):

        from rest_framework import serializers

        class AktivitasSerializer(
            serializers.ModelSerializer
        ):

            class Meta:

                model = AktivitasPegawai

                fields = "__all__"

                read_only_fields = [
                    "id",
                    "created_at",
                    "updated_at",
                ]

        return AktivitasSerializer(
            instance=instance,
            data=data,
            partial=partial
        )

 

# ============================================================
# PENGADUAN
# ============================================================

class PengaduanViewSet(viewsets.ModelViewSet):

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = PengaduanSerializer

    queryset = Pengaduan.objects.all()

    def get_queryset(self):
        return filter_by_group(
            request=self.request,
            queryset=Pengaduan.objects.all(),
            owner_field="pelapor"
        )
    @extend_schema(
        tags=["Pengaduan"],
        parameters=[
            OpenApiParameter(
                name="search",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Keyword pencarian"
            ),
            OpenApiParameter(
                name="page",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Nomor halaman"
            ),
            OpenApiParameter(
                name="page_size",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Jumlah data per halaman"
            ),
            OpenApiParameter(
                name="bygroup",
                type=str,
                enum=["group", "pribadi"],
                location=OpenApiParameter.QUERY,
                description="Default: group"
            ),
            OpenApiParameter(
                name="status",
                type=str,
                enum=[
                    "BARU",
                    "VERIFIKASI",
                    "PIMPINAN",
                    "PROSES",
                    "MONITORING",
                    "SELESAI",
                    "DITUTUP",
                    "DITOLAK",
                ],
                location=OpenApiParameter.QUERY,
                description="Filter status"
            ),

            OpenApiParameter(
                name="pelapor",
                type=str,
                enum=["group", "pribadi"],
                location=OpenApiParameter.QUERY,
                description="Filter pelapor"
            ),

            OpenApiParameter(
                name="petugas",
                type=str,
                enum=["group", "pribadi"],
                location=OpenApiParameter.QUERY,
                description="Filter petugas"
            ),

            OpenApiParameter(
                name="verifikator",
                type=str,
                enum=["true", "false"],
                location=OpenApiParameter.QUERY,
                description="Sudah diverifikasi atau belum"
            ),
        ],
    )
    def list(self, request):

        queryset = (
            self.get_queryset()
            .order_by("-created_at")
        )

        return success_response(
            data=search_and_paginate(
                request=request,
                queryset=queryset,
                search_fields=[
                    "status",
                    "judul",
                    "uraian",
                ]
            )
        )

    @extend_schema(
        tags=["Pengaduan"],
        responses=PengaduanSerializer
    )
    def retrieve(
        self,
        request,
        pk=None
    ):

        obj = self.get_object()

        return success_response(
            data=serialize_model(obj)
        )

    @extend_schema(
        tags=["Pengaduan"],
        request=PengaduanCreateSerializer,
        responses=PengaduanSerializer,
    )
    def create(
        self,
        request
    ):

        serializer = PengaduanCreateSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return error_response(
                "Data pengaduan tidak valid.",
                serializer.errors
            )

        user = request.user

        obj = Pengaduan.objects.create(
            nomor_tiket=generateNomorTiket(),
            pelapor=user,
            nama_pelapor=user.get_full_name()
            or user.username,
            hp_pelapor=user.no_hp or "",
            judul=serializer.validated_data[
                "judul"
            ],
            desa_id=serializer.validated_data[
                "desa"
            ],
            lokasi_kejadian=serializer.validated_data[
                "lokasi_kejadian"
            ],
            uraian=serializer.validated_data[
                "uraian"
            ],
            lampiran=request.FILES.get(
                "lampiran"
            ),
            waktu_kejadian = serializer.validated_data["tanggal"],
            status="BARU",
            source="ANDROID",
        )

        return success_response(
            data=serialize_model(obj),
            message="Pengaduan berhasil dibuat.",
            status_code=status.HTTP_201_CREATED
        )

    @extend_schema(
        tags=["Pengaduan"]
    )
    @action(
        detail=True,
        methods=["get"]
    )
    def riwayat(
        self,
        request,
        pk=None
    ):

        pengaduan = self.get_object()

        history = (
            PengaduanHistory.objects
            .filter(
                pengaduan=pengaduan
            )
            .order_by(
                "-created_at"
            )
        )

        return success_response(
            data=[
                serialize_model(item)
                for item in history
            ]
        )

    @extend_schema(
        tags=["Pengaduan"]
    )
    @action(
        detail=True,
        methods=["get"]
    )
    def lampiran(
        self,
        request,
        pk=None
    ):

        pengaduan = self.get_object()

        lampiran = (
            LampiranPengaduan.objects
            .filter(
                pengaduan=pengaduan
            )
        )

        return success_response(
            data=[
                serialize_model(item)
                for item in lampiran
            ]
        )

    @extend_schema(
        tags=["Pengaduan"],
        request=PengaduanVerifikasiSerializer,
    )
    @action(
        detail=True,
        methods=["post"]
    )
    def verifikasi(
        self,
        request,
        pk=None
    ):

        serializer = (
            PengaduanVerifikasiSerializer(
                data=request.data
            )
        )

        if not serializer.is_valid():

            return error_response(
                "Data tidak valid.",
                serializer.errors
            )

        pengaduan = self.get_object()

        try:

            petugas = User.objects.get(
                pk=serializer.validated_data[
                    "petugas"
                ]
            )

        except User.DoesNotExist:

            return error_response(
                "Petugas tidak ditemukan."
            )

        pengaduan.petugas = petugas

        pengaduan.disposisi_oleh = (
            request.user
        )

        pengaduan.tindak_lanjut = (
            serializer.validated_data.get(
                "catatan",
                ""
            )
        )

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
            user=petugas,
            judul="Pengaduan Diverifikasi",
            deskripsi=(
                "Pengaduan telah dialihkan "
                "ke bidang terkait untuk "
                "ditindaklanjuti"
            ),
            status_lama="",
            status_baru="VERIFIKASI",
            latitude=pengaduan.latitude,
            longitude=pengaduan.longitude
        )

        Notifikasi.objects.create(
            user=petugas,
            judul=pengaduan.judul,
            pesan=pengaduan.tindak_lanjut,
            url=f"/pengaduan/{pengaduan.id}/"
        )

        return success_response(
            data=serialize_model(
                pengaduan
            ),
            message="Pengaduan berhasil diverifikasi."
        )
    @extend_schema(
        tags=["Pengaduan"],
        request=PengaduanStatusSerializer,
    )
    @action(
        detail=True,
        methods=["put"]
    )
    def status(
        self,
        request,
        pk=None
    ):

        serializer = PengaduanStatusSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return error_response(
                "Data tidak valid.",
                serializer.errors
            )

        pengaduan = self.get_object()

        status_lama = pengaduan.status

        pengaduan.status = (
            serializer.validated_data[
                "status"
            ]
        )

        pengaduan.save()

        PengaduanHistory.objects.create(
            pengaduan=pengaduan,
            user=request.user,
            judul="Perubahan Status",
            deskripsi=(
                f"Status diubah dari "
                f"{status_lama} menjadi "
                f"{pengaduan.status}"
            ),
            status_lama=status_lama,
            status_baru=pengaduan.status,
            latitude=pengaduan.latitude,
            longitude=pengaduan.longitude,
        )

        return success_response(
            data=serialize_model(
                pengaduan
            ),
            message="Status berhasil diperbarui."
        )
    @extend_schema(
        tags=["Pengaduan"],
        request=PengaduanProcessSerializer
    )
    @action(
        detail=True,
        methods=["post"]
    )
    def proses(
        self,
        request,
        pk=None
    ):

        user = request.user

        group = user.groups.first()

        if not (
            user.is_superuser
            or (
                group
                and group.name in [
                    "ADMIN",
                    "KABAN",
                    "KABID"
                ]
            )
        ):

            return error_response(
                "Anda tidak memiliki akses untuk memproses pengaduan.",
                status_code=status.HTTP_403_FORBIDDEN
            )

        pengaduan = self.get_object()

        status_baru = request.data.get(
            "status"
        )

        if status_baru:

            pengaduan.status = status_baru

        if hasattr(
            pengaduan,
            "petugas"
        ):

            petugas_id = request.data.get(
                "petugas"
            )

            if petugas_id:

                try:

                    pengaduan.petugas_id = (
                        petugas_id
                    )

                except Exception:
                    pass

        if hasattr(
            pengaduan,
            "verifikator"
        ):

            pengaduan.verifikator = user

        if hasattr(
            pengaduan,
            "verified_at"
        ):

            pengaduan.verified_at = (
                timezone.now()
            )

        pengaduan.save()

        return success_response(
            data=serialize_model(
                pengaduan
            ),
            message="Pengaduan berhasil diproses."
        )
    @extend_schema(
        tags=["Pengaduan"]
    )
    @action(
        detail=False,
        methods=["get"]
    )
    def total(
        self,
        request
    ):

        user = request.user

        return success_response(
            data={
                "umum": {
                    "total": Pengaduan.objects.count(),
                    "baru": Pengaduan.objects.filter(
                        status="BARU"
                    ).count(),
                    "selesai": Pengaduan.objects.filter(
                        status="SELESAI"
                    ).count(),
                    "berproses": Pengaduan.objects.exclude(
                        status__in=[
                            "BARU",
                            "SELESAI",
                        ]
                    ).count(),
                },
                "foryou": {
                    "total": Pengaduan.objects.filter(
                        petugas=user
                    ).count(),
                    "aktif": Pengaduan.objects.filter(
                        petugas=user
                    ).exclude(
                        status="SELESAI"
                    ).count(),
                    "selesai": Pengaduan.objects.filter(
                        petugas=user,
                        status="SELESAI"
                    ).count(),
                },
                "fromyou": {
                    "total": Pengaduan.objects.filter(
                        pelapor=user
                    ).count(),
                    "aktif": Pengaduan.objects.filter(
                        pelapor=user
                    ).exclude(
                        status="SELESAI"
                    ).count(),
                    "selesai": Pengaduan.objects.filter(
                        pelapor=user,
                        status="SELESAI"
                    ).count(),
                }
            }
        )
# ============================================================
# ORGANISASI
# ============================================================

class OrganisasiViewSet(
    viewsets.ModelViewSet
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = (
        Organisasi.objects.all()
    )

    def get_queryset(self):

        user = self.request.user

        if user.is_superuser:

            return Organisasi.objects.all()

        group = user.groups.first()

        if group and group.name in [
            "ADMIN",
            "KABAN",
            "KABID"
        ]:

            return Organisasi.objects.all()

        return Organisasi.objects.filter(
            ketua=user
        )

    def list(self, request):

        return success_response(
            data=[
                serialize_model(item)
                for item in self.get_queryset()
            ]
        )

    def retrieve(
        self,
        request,
        pk=None
    ):

        obj = self.get_object()

        return success_response(
            data=serialize_model(obj)
        )

    @extend_schema(
        tags=["Organisasi"]
    )
    @action(
        detail=True,
        methods=["get"]
    )
    def anggota(
        self,
        request,
        pk=None
    ):

        organisasi = self.get_object()

        anggota = (
            AnggotaOrganisasi.objects.filter(
                organisasi=organisasi
            )
        )

        return success_response(
            data=[
                serialize_model(item)
                for item in anggota
            ]
        )

    @extend_schema(
        tags=["Organisasi"]
    )
    @action(
        detail=True,
        methods=["get"]
    )
    def dokumen(
        self,
        request,
        pk=None
    ):

        organisasi = self.get_object()

        dokumen = (
            DokumenOrganisasi.objects.filter(
                organisasi=organisasi
            )
        )

        return success_response(
            data=[
                serialize_model(item)
                for item in dokumen
            ]
        )


# ============================================================
# NOTIFIKASI
# ============================================================

class NotifikasiViewSet(
    viewsets.ReadOnlyModelViewSet
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = (
        Notifikasi.objects.all()
    )

    def get_queryset(self):

        return Notifikasi.objects.filter(
            user=self.request.user
        ).order_by(
            "-created_at"
        )

    def list(self, request):

        return success_response(
            data=[
                serialize_model(item)
                for item in self.get_queryset()
            ]
        )

    def retrieve(
        self,
        request,
        pk=None
    ):

        obj = self.get_object()

        return success_response(
            data=serialize_model(obj)
        )

    @extend_schema(
        tags=["Notifikasi"]
    )
    @action(
        detail=True,
        methods=["post"]
    )
    def read(
        self,
        request,
        pk=None
    ):

        notification = self.get_object()

        notification.status_baca = True

        notification.save()

        return success_response(
            message="Notifikasi sudah dibaca."
        )

    @extend_schema(
        tags=["Notifikasi"]
    )
    @action(
        detail=False,
        methods=["post"]
    )
    def read_all(
        self,
        request
    ):

        Notifikasi.objects.filter(
            user=request.user,
            status_baca=False
        ).update(
            status_baca=True
        )

        return success_response(
            message="Semua notifikasi sudah dibaca."
        )


# ============================================================
# DEVICE TOKEN / FCM
# ============================================================

class DeviceTokenViewSet(
    viewsets.ViewSet
):

    permission_classes = [
        IsAuthenticated
    ]

    @extend_schema(
        tags=["Device Token / FCM"],
        request=DeviceTokenSerializer,
    )
    def create(
        self,
        request
    ):

        serializer = DeviceTokenSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return error_response(
                "Data tidak valid.",
                serializer.errors
            )

        device_token, created = (
            DeviceToken.objects.update_or_create(
                token=serializer.validated_data[
                    "token"
                ],
                defaults={
                    "user": request.user,
                    "platform": "ANDROID",
                    "is_active": True,
                    "last_used_at": timezone.now(),
                }
            )
        )

        return success_response(
            data={
                "created": created,
                "device": serialize_model(
                    device_token
                )
            },
            message="Device token berhasil disimpan."
        )

    @extend_schema(
        tags=["Device Token / FCM"]
    )
    def list(
        self,
        request
    ):

        return success_response(
            data=[
                serialize_model(item)
                for item in DeviceToken.objects.filter(
                    user=request.user,
                    is_active=True
                )
            ]
        )

# ============================================================
# BERITA
# ============================================================

class BeritaViewSet(
    viewsets.ReadOnlyModelViewSet
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = (
        MateriBerita.objects.all()
    )

    def list(self, request):

        queryset = (
            MateriBerita.objects
            .filter(
                is_public=True,
                status_publish=True
            )
            .order_by(
                "-published_at"
            )
        )

        return success_response(
            data=[
                serialize_model(item)
                for item in queryset
            ]
        )

    def retrieve(
        self,
        request,
        pk=None
    ):

        obj = self.get_object()

        return success_response(
            data=serialize_model(obj)
        )


# ============================================================
# MASTER DATA
# ============================================================

class KecamatanViewSet(
    viewsets.ReadOnlyModelViewSet
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = Kecamatan.objects.all()

    def list(self, request):

        return success_response(
            data=[
                serialize_model(item)
                for item in self.get_queryset()
            ]
        )


class DesaViewSet(
    viewsets.ReadOnlyModelViewSet
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = Desa.objects.all()

    def list(self, request):

        return success_response(
            data=[
                serialize_model(item)
                for item in self.get_queryset()
            ]
        )
class PetugasViewSet(
    viewsets.ReadOnlyModelViewSet
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = User.objects.filter(
        is_active=True
    ).exclude(
        groups__name__iexact="MASYARAKAT"
    ).distinct()

    def list(self, request):

        return success_response(
            data=[
                {
                    "id": item.id,
                    "nama": (
                        item.get_full_name()
                        or item.username
                    ),
                    # "username": item.username,
                    # "nik": item.nik,
                    # "no_hp": item.no_hp,
                }
                for item in self.get_queryset()
            ]
        ) 
class DinasViewSet(
    viewsets.ReadOnlyModelViewSet
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = Dinas.objects.all()

    def list(self, request):

        return success_response(
            data=[
                serialize_model(item)
                for item in self.get_queryset()
            ]
        )


class BidangViewSet(
    viewsets.ReadOnlyModelViewSet
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = Bidang.objects.all()

    def list(self, request):

        return success_response(
            data=[
                serialize_model(item)
                for item in self.get_queryset()
            ]
        )


class JenisOrganisasiViewSet(
    viewsets.ReadOnlyModelViewSet
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = JenisOrganisasi.objects.all()

    def list(self, request):

        return success_response(
            data=[
                serialize_model(item)
                for item in self.get_queryset()
            ]
        )


class JenisKasusViewSet(
    viewsets.ReadOnlyModelViewSet
):

    permission_classes = [
        IsAuthenticated
    ]

    queryset = JenisKasus.objects.all()

    def list(self, request):

        return success_response(
            data=[
                serialize_model(item)
                for item in self.get_queryset()
            ]
        ) 