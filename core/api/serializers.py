
from rest_framework import serializers

from core.apps.accounts.User.models import User
from core.apps.pengaduan.models import Pengaduan
from core.apps.master.Desa.models import Desa

 
class PengaduanStatusSerializer(
    serializers.Serializer
):
    status = serializers.ChoiceField(
        choices=[
            "BARU",
            "VERIFIKASI",
            "PIMPINAN",
            "PROSES",
            "MONITORING",
            "SELESAI",
            "DITUTUP",
            "DITOLAK",
        ]
    )
class PengaduanVerifikasiSerializer(
    serializers.Serializer
):
    petugas = serializers.IntegerField()

    catatan = serializers.CharField(
        required=False,
        allow_blank=True
    )
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "nik",
            "no_hp",
            "is_active",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "date_joined",
            "is_active",
        ]
# ============================================================
# AUTH
# ============================================================

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True
    )


class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = serializers.DictField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class RefreshTokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        required=False,
        allow_blank=True
    )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True
    )

    new_password = serializers.CharField(
        write_only=True
    )

    new_password_confirmation = serializers.CharField(
        write_only=True
    )


# ============================================================
# PROFILE
# ============================================================

class ProfileUpdateSerializer(serializers.Serializer):

    first_name = serializers.CharField(
        required=False
    )

    last_name = serializers.CharField(
        required=False
    )

    email = serializers.EmailField(
        required=False
    )

    nik = serializers.CharField(
        required=False
    )

    no_hp = serializers.CharField(
        required=False
    )


# ============================================================
# DEVICE TOKEN / FCM
# ============================================================

class DeviceTokenSerializer(serializers.Serializer):

    token = serializers.CharField()

    platform = serializers.CharField(
        required=False,
        default="android"
    )


class DeviceTokenDeleteSerializer(serializers.Serializer):

    token = serializers.CharField(
        required=False,
        allow_blank=True
    )


# ============================================================
# PENGADUAN
# ============================================================

class PengaduanProcessSerializer(serializers.Serializer):

    status = serializers.CharField(
        required=False
    )

    petugas = serializers.IntegerField(
        required=False,
        allow_null=True
    ) 

class ProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    nik = serializers.CharField(required=False)
    no_hp = serializers.CharField(required=False)

class PengaduanSerializer(serializers.ModelSerializer):

    judul = serializers.CharField(
        help_text="Judul Pengaduan"
    )

    desa = serializers.PrimaryKeyRelatedField(
        queryset=Desa.objects.all(),
        help_text="Pilih Desa"
    )

    lokasi_kejadian = serializers.CharField(
        help_text="Lokasi Kejadian"
    )

    uraian = serializers.CharField(
        help_text="Uraian Pengaduan"
    )

    lampiran = serializers.FileField(
        required=False,
        allow_null=True
    )

    waktu_kejadian = serializers.DateTimeField(
        required=False
    )

    class Meta:
        model = Pengaduan
        fields = "__all__"
        read_only_fields = [
            "id",
            "nomor_tiket",
            "pelapor",
            "status",
            "source",
            "created_at",
            "updated_at",
        ]
class PengaduanCreateSerializer(
    serializers.Serializer
):
    judul = serializers.CharField()

    desa = serializers.IntegerField()

    lokasi_kejadian = serializers.CharField()

    uraian = serializers.CharField()

    tanggal = serializers.DateTimeField()

    lampiran = serializers.FileField(
        required=False,
        allow_null=True
    )
class PengaduanProcessSerializer(
    serializers.Serializer
):
    status = serializers.CharField(
        required=False
    )

    petugas = serializers.IntegerField(
        required=False
    )