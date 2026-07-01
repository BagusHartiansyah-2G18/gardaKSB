# core/context_processors.py

from core.utils import subMenu

def menu_legalitas(request):
    return {
        "menu_legalitas": subMenu()
    }