from django import forms
from core.apps.accounts.User.models import User

class VerifikasiForm(forms.Form):

    petugas = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label="Petugas Pengawal"
    )

    catatan = forms.CharField(
        widget=forms.Textarea,
        required=False
    )

 
from core.apps.organisasi.models import Organisasi
class UploadDokumenOrganisasiForm(forms.Form):

    organisasi = forms.ModelChoiceField(
        queryset=Organisasi.objects.all()
    )

    def __init__(self, *args, **kwargs):
        persyaratan = kwargs.pop("persyaratan", [])
        super().__init__(*args, **kwargs)

        for item in persyaratan:
            self.fields[f"persyaratan_{item.id}"] = forms.FileField(
                label=item.nama,
                required=not item.wajib
            )