from rest_framework import serializers
from .models import Tunnel, Pool, Address, Policy


class AddressDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class PoolListSerializer(serializers.ModelSerializer):
    addresses = AddressDetailSerializer(read_only=True, many=True)
    class Meta:
        model = Pool
        fields = [
            'id',
            'name',
            'address_range',
            'addresses',
        ]


class PoolDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        fields = '__all__'


class PolicyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'


class TunnelListSerializer(serializers.ModelSerializer):
    pools = PoolDetailSerializer(read_only=True, many=True)
    policies = PolicyDetailSerializer(read_only=True, many=True)
    class Meta:
        model = Tunnel
        fields = [
            'id',
            'name',
            'updated',
            'approval',
            'url',
            'pools',
            'policies',
            'auth_server',
        ]


class TunnelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tunnel
        fields = '__all__'
