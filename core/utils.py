from django.db.models.functions import Coalesce
from django.db.models import Sum,Count,Q,F,Value ,DecimalField
from django.db.models.functions import ExtractMonth  
import requests
import aiohttp
from aiohttp import FormData

def setKeyGroup(
        admin=None,
        kaban=None,
        sekban=None,
        kabid=None,
        anggota=None,
        publik=None,
    ):
    data = {
        "ADMIN": admin,
        "KABAN": kaban,
        "SEKBAN": sekban,
        "KABID": kabid,
        "ANGGOTA": anggota,
        "PUBLIK": publik,
    }

    return {
        k: v
        for k, v in data.items()
        if v is not None
    }

def filterData(request, qs, **kwargs):
    if request.user.is_superuser:
        return qs
    groupUser =request.user.groups.first()
    groupKey = kwargs.get("groupKey")
    if groupKey:
        groupData = kwargs.get("groupData")
        qs = filterByGroup(request,qs,[groupKey,groupData.get(groupUser.name)])
        print(qs)
    
    return qs
def filterByGroup(request, qs, key=None):

    if not key or len(key) < 2:
        return qs

    field, value = key

    if value is None:
        return qs.none()

    return qs.filter(
        **{
            field: value
        }
    )
def aksesMenuAdmin(request):
    if request.user.is_superuser:
        return True

    return request.user.groups.filter(
        name__in=[
            "ADMIN",
            "KABAN",
            "SEKBAN"
        ]
    ).exists()