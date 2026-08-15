
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    LoginAPIView,
    LogoutAPIView,
    RefreshAPIView,
    MeAPIView,
    ProfileAPIView,
    ChangePasswordAPIView,
    DashboardAPIView,
    AktivitasViewSet,
    PengaduanViewSet,
    OrganisasiViewSet,
    NotifikasiViewSet,
    DeviceTokenViewSet,
    BeritaViewSet,
    KecamatanViewSet,
    DesaViewSet,
    DinasViewSet,
    BidangViewSet,
    JenisOrganisasiViewSet,
    JenisKasusViewSet,
    PetugasViewSet,
)


router = DefaultRouter()


router.register(
    "device-token",
    DeviceTokenViewSet,
    basename="device-token"
)
router.register(
    "aktivitas",
    AktivitasViewSet,
    basename="aktivitas"
)

router.register(
    "pengaduan",
    PengaduanViewSet,
    basename="pengaduan"
)

router.register(
    "organisasi",
    OrganisasiViewSet,
    basename="organisasi"
)

router.register(
    "notifikasi",
    NotifikasiViewSet,
    basename="notifikasi"
)

router.register(
    "berita",
    BeritaViewSet,
    basename="berita"
)

router.register(
    "master/kecamatan",
    KecamatanViewSet,
    basename="kecamatan"
)
router.register(
    "master/petugas",
    PetugasViewSet,
    basename="petugas"
)
router.register(
    "master/desa",
    DesaViewSet,
    basename="desa"
)

router.register(
    "master/dinas",
    DinasViewSet,
    basename="dinas"
)

router.register(
    "master/bidang",
    BidangViewSet,
    basename="bidang"
)

router.register(
    "master/jenis-organisasi",
    JenisOrganisasiViewSet,
    basename="jenis-organisasi"
)

router.register(
    "master/jenis-kasus",
    JenisKasusViewSet,
    basename="jenis-kasus"
)


urlpatterns = [

    # ==========================
    # AUTHENTICATION
    # ==========================

    path(
        "auth/login/",
        LoginAPIView.as_view(),
        name="login"
    ),

    path(
        "auth/logout/",
        LogoutAPIView.as_view(),
        name="logout"
    ),

    path(
        "auth/refresh/",
        RefreshAPIView.as_view(),
        name="refresh"
    ),

    path(
        "auth/me/",
        MeAPIView.as_view(),
        name="me"
    ),

    path(
        "auth/change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password"
    ),

    # ==========================
    # PROFILE
    # ==========================

    path(
        "profile/",
        ProfileAPIView.as_view(),
        name="profile"
    ),

    # ==========================
    # DASHBOARD
    # ==========================

    path(
        "dashboard/",
        DashboardAPIView.as_view(),
        name="dashboard"
    ),

    # ==========================
    # DEVICE TOKEN
    # ==========================

     

    # ==========================
    # ROUTER
    # ==========================

    path(
        "",
        include(router.urls)
    ),
]