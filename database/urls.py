from django.urls import path
from . import views

urlpatterns = [
    path('ravpn/delete/<uuid:id>/', views.delete_vpn, name='delete_vpn'),
    path('ravpn/tunnel/<uuid:id>/', views.TunnelRetrieveView.as_view(), name='tunnel_detail'),
    path('ravpn/tunnels/', views.TunnelListView.as_view(), name='tunnel_list'),
    path('ravpn/config/pull/', views.config_pull, name='config_pull'),
    path('ravpn/config/parse/', views.config_parse, name='config_parse'),
    path('', views.database, name='database'),
]