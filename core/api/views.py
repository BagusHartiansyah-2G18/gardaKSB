
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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


from drf_spectacular.utils import extend_schema
from .serializers import *

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
        except Exception:
            value = None

        data[field_name] = serialize_value(
            value
        )

    return data


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

        user = self.request.user

        group = user.groups.first()

        if user.is_superuser:

            return Pengaduan.objects.all()

        if group and group.name in [
            "ADMIN",
            "KABAN",
            "KABID"
        ]:

            return Pengaduan.objects.all()

        return Pengaduan.objects.filter(
            pelapor=user
        )

    @extend_schema(
        tags=["Pengaduan"],
        responses=PengaduanSerializer(many=True)
    )
    def list(self, request):

        queryset = self.get_queryset()

        return success_response(
            data=[
                serialize_model(item)
                for item in queryset.order_by(
                    "-created_at"
                )
            ]
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
        request=PengaduanSerializer,
        responses=PengaduanSerializer
    )
    def create(
        self,
        request
    ):

        serializer = PengaduanSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return error_response(
                "Data pengaduan tidak valid.",
                serializer.errors
            )

        obj = serializer.save(
            pelapor=request.user
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
        tags=["Pengaduan"]
    )
    @action(
        detail=True,
        methods=["get"]
    )
    def verifikasi(
        self,
        request,
        pk=None
    ):

        pengaduan = self.get_object()

        verifikasi = (
            VerifikasiPengaduan.objects
            .filter(
                pengaduan=pengaduan
            )
            .order_by(
                "-tanggal_verifikasi"
            )
        )

        return success_response(
            data=[
                serialize_model(item)
                for item in verifikasi
            ]
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

class DeviceTokenAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @extend_schema(
        tags=["Device Token / FCM"],
        request=DeviceTokenSerializer,
    )
    def post(self, request):

        token = request.data.get(
            "token"
        )

        platform = request.data.get(
            "platform",
            "android"
        )

        if not token:

            return error_response(
                "Token perangkat wajib diisi."
            )

        device = (
            DeviceToken.objects
            .filter(
                token=token
            )
            .first()
        )

        if device:

            device.user = request.user
            device.platform = platform
            device.is_active = True

            if hasattr(
                device,
                "last_used_at"
            ):

                device.last_used_at = (
                    timezone.now()
                )

            device.save()

        else:

            device = DeviceToken.objects.create(
                user=request.user,
                token=token,
                platform=platform,
                is_active=True
            )

        return success_response(
            data=serialize_model(
                device
            ),
            message="Device token berhasil disimpan."
        )

    @extend_schema(
        tags=["Device Token / FCM"],
        request=DeviceTokenDeleteSerializer,
    )
    def delete(
        self,
        request
    ):

        token = request.data.get(
            "token"
        )

        queryset = DeviceToken.objects.filter(
            user=request.user
        )

        if token:

            queryset = queryset.filter(
                token=token
            )

        queryset.update(
            is_active=False
        )

        return success_response(
            message="Device token dinonaktifkan."
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