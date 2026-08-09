"""
URL configuration for kawal_LPMD project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from core.views import (
    home,pengaduan,informasi,kirimPengaduan,
    trackingPengaduan,detailInformasi,materiBidang,
    addViewBerita
)
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        "api/",
        include("core.api.urls")
    ),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema'
        ),
        name='swagger-ui'
    ),

    path( "api/", include("core.urlAPI") ),
    # publik 
    path('', home, name='home_default'),
    path('pengaduan/', pengaduan, name='pengaduan'),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('informasi/<str:kategori>/', informasi, name='informasi'),
    path('pengaduan/kirim/', kirimPengaduan, name="kirimPengaduan"), 
    path('tracking/<str:nomor_tiket>/', trackingPengaduan, name="trackingPengaduan"), 
    path('informasi/detail/<slug:slug>/', detailInformasi,name="detailInformasi"),
    path('informasi/materi/<slug:slug>/', materiBidang,name="materiBidang"),
    path('informasi/materi/<slug:slug>/<str:id>/', materiBidang,name="materiBidangs"),
   
    path('addViewBerita/<str:id>/<str:aktivitas>/', addViewBerita, name='addLikeBerita'),
    
    path(
        "firebase-messaging-sw.js",
        TemplateView.as_view(
            template_name="firebase-messaging-sw.js",
            content_type="application/javascript",
        ),
        name="firebase-sw",
    ),
    # path('dashboard/', dashboard, name="dashboard"),
    # path('kelompok/<str:jenis>/', pkelompok, name="pkelompok"),
    # path('kelompok/detail/<int:id>/',pkelompokDetail, name='kelompok_detail'),
    # path('usaha/', pusaha, name="pusaha"),
    # path('sigin/', login_view, name='sigin'),
    # path('pendapatan/<int:id>/<str:jenis>/', pkeuangan, name='pendapatan'),
    # path(
    #     'pendapatan/<int:id>/<str:jenis>/add/',
    #     pkeuanganAdd,
    #     name='pkeuanganAdd'
    # ),
    
    # path(
    #     "api/sync",
    #     compareDataKelompok,
    #     name="compareDataKelompok"
    # ),

    # path(
    #     'ajax/item-legalitas/',
    #     ajaxItemLegalitas,
    #     name='ajaxItemLegalitas'
    # ),

    # path("chaining/", include("smart_selects.urls")),

    # path(
    #     'pendapatan/edit/<int:id>/<str:jenis>/',
    #     pkeuanganEdit,
    #     name='pkeuanganEdit'
    # ),
    # path('pendapatan/approve/<int:id>/<str:key>/', pendapatanApprove, name='pendapatanApprove'),
    
    # path('legalitas/approve/<int:id>/<str:key>/', legalitasApprove, name='legalitasApprove'),
    
    # path("__reload__/", include("django_browser_reload.urls")),
    # path('accounts/', include('django.contrib.auth.urls')),

    
    # path('kelompok/<int:id>/anggota/add/', pkelompokAnggotaAdd, name='anggota_add'),
    # path('kelompok/<int:id>/aset/add/', pkelompoAsetAdd, name='aset_add'),
    
    # path('anggota/<int:id>/delete/', anggota_delete, name='anggota_delete'),
    # path('aset/<int:id>/delete/', aset_delete, name='aset_delete'),
    # path('early/', early, name='early'),


    # path('monitor/<str:idJLega>/', pmonitor, name="pmonitor"),
    # path('monitor/legalitas/<str:idJLega>/', pmonitorLegalitas, name="pmonitorLegalitas"),
    # path('monitor/aset/<str:idJLega>/', pmonitorAset, name="pmonitorAset"),
    # path('monitor/aproval/<str:idJLega>/', pmonitorAproval, name="pmonitorAproval"),
    # path('monitor/laporan/<str:idJLega>/', pmonitorLaporan, name="laporan"),

    # path('<str:idJLega>/', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
) 