
from rest_framework import serializers
from .models import Kecamatan, Desa

class KecamatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kecamatan
        fields = ['id', 'nmKec']


class DesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desa
        fields = ['id', 'nmDesa', 'kecamatan']
