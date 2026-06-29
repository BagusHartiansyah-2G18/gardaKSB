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

from core.views import home,login,login_view,seed_sumbawa,dashboard
from core.apps.kelompok.vkelompok import pkelompok,pkelompokDetail,pkelompoAsetAdd,pkelompokAnggotaAdd,anggota_delete,aset_delete,legalitasApprove
from core.apps.usaha.vusaha import pusaha
from core.apps.keuangan.vkeuangan import pkeuangan,pkeuanganAdd




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('login/', login),
    path('seed-sumbawa/', seed_sumbawa),
    path('dashboard/', dashboard, name="dashboard"),
    path('kelompok/', pkelompok, name="pkelompok"),
    path('kelompok/<int:id>/',pkelompokDetail, name='kelompok_detail'),
    path('usaha/', pusaha, name="pusaha"),
    path('sigin/', login_view, name='sigin'),
    path('pendapatan/<int:id>/', pkeuangan, name='pendapatan'),
    path('pendapatan/add', pkeuanganAdd, name='pkeuanganAdd'),
    
    path('legalitas/approve/<int:id>/<str:key>/', legalitasApprove, name='legalitasApprove'),
    
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('django.contrib.auth.urls')),

    
    path('kelompok/<int:id>/anggota/add/', pkelompokAnggotaAdd, name='anggota_add'),
    path('kelompok/<int:id>/aset/add/', pkelompoAsetAdd, name='aset_add'),
    
    path('anggota/<int:id>/delete/', anggota_delete, name='anggota_delete'),
    path('aset/<int:id>/delete/', aset_delete, name='aset_delete'),



]
