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
