from rest_framework import serializers
from .models import Tunnel

class TunnelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tunnel
        fields = [
            'id',
            'name',
            'updated',
            'approval',
            'url',
        ]

class TunnelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tunnel
        fields = '__all__'