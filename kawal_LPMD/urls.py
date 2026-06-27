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
from core.apps.kelompok.vkelompok import pkelompok
from core.apps.usaha.vusaha import pusaha
from core.apps.keuangan.vkeuangan import pkeuangan,pkeuanganAdd




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('login', login),
    path('seed-sumbawa/', seed_sumbawa),
    path('dashboard', dashboard, name="dashboard"),
    path('kelompok', pkelompok, name="pkelompok"),
    path('usaha', pusaha, name="pusaha"),
    path('sigin', login_view, name='sigin'),
    path('pendapatan', pkeuangan, name='pendapatan'),
    path('pendapatan/add', pkeuanganAdd, name='pkeuanganAdd'),
    

    
    path("__reload__/", include("django_browser_reload.urls")),
]
