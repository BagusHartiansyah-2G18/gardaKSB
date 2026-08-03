# core/context_processors.py

# from core.utils import subMenu
from core.apps.master.Bidang.service import getBidang

def menu_legalitas(request):
    return {
        "dbidang": getBidang()
    }