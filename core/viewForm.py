from django import forms

from core.apps.accounts.User.models import User


class VerifikasiPengaduanForm(forms.Form):

    petugas = forms.ModelChoiceField(
        queryset=User.objects.filter(
            is_active=True
        ),
        label="Petugas"
    )

    catatan = forms.CharField(
        required=False,
        widget=forms.Textarea
    )