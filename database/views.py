from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import generics
from .fw_cmd import asafw
from .models import Tunnel
from .serializers import TunnelListSerializer, TunnelDetailSerializer

# Create your views here.
def database(request):
    return HttpResponse("<h3>Hi curious buddy!</h3>")


def config_pull(request):
    config_file = asafw.run_config()
    return HttpResponse(config_file)

config_file = './database/fw_cmd/config_output/output.txt'
def config_parse(request):
    test = asafw.parse_asa(config_file)
    return HttpResponse(test)

def delete_vpn(request, id):
    try:
        script = ''
        tunnel = get_object_or_404(Tunnel, id=id)
        policies = tunnel.policies.all()
        for policy in policies:
            script = script + f'''
            group-policy {policy.name} attributes\n
            no group-lock value {tunnel.name}\n
            exit\n
            '''
        return HttpResponse(script)
    except:
        return HttpResponse('Not Found')

class TunnelListView(generics.ListAPIView):
    queryset = Tunnel.objects.all()
    serializer_class = TunnelListSerializer


class TunnelRetrieveView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Tunnel.objects.all()
    serializer_class = TunnelDetailSerializer