from core.apps.informasi.MateriBerita.models import MateriBerita
from core.apps.informasi.MateriBeritaActivity.models import MateriBeritaActivity
from django.db.models import Count, Exists, OuterRef,  Q
from core.apps.accounts.User.models import User 
from core.apps.accounts.models import UserProfile 

from core.utilsData import PEGAWAI
from core.apps.master.Bidang.models import Bidang
from django.shortcuts import get_object_or_404 
from django.db.models.functions import ExtractMonth 

def getUserByID(id):
    return UserProfile.objects.select_related(
        "user",
        "desa",
        "desa__kecamatan",
        "bidang",
        "bidang__dinas",
    ).filter(
        user_id=id
    ).first()
    
def getAllID(id): 
    profile = getUserByID(id)
    if not profile:
        return None
    profile.idBidang = getattr(profile.bidang, "id", None)
    profile.idDesa = getattr(profile.desa, "id", None)

    profile.idKecamatan = (
        profile.desa.kecamatan.id
        if profile.desa and profile.desa.kecamatan
        else None
    )

    profile.idDinas = (
        profile.bidang.dinas.id
        if profile.bidang and profile.bidang.dinas
        else None
    )

    return profile

def getUserAttrID(obj, attr):
    return getattr(obj, attr, None).id if getattr(obj, attr, None) else None



def insertUserPegawai(data):

    username = data["nip"]

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "first_name": data["nama"],
            "nik": data["nip"],
            "no_hp": data["noTelp"] or "",
            "is_active": True,
        }
    )

    # update data user
    user.first_name = data["nama"]
    user.nik = data["nip"]
    user.no_hp = data["noTelp"] or ""
    user.save()

    bidang = None

    if data.get("bidangId"):
        bidang = Bidang.objects.filter(
            id=data["bidangId"]
        ).first()

    profile, created_profile = UserProfile.objects.get_or_create(
        user=user
    )

    profile.bidang = bidang
    profile.save()

    return {
        "user": user,
        "profile": profile,
        "created": created,
        "created_profile": created_profile,
    }

def addDataPegawai():
    for item in PEGAWAI:
        insertUserPegawai(item)