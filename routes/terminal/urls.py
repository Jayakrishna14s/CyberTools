from django.urls import path, include # type: ignore
from django.contrib import admin # type: ignore
from routes.terminal import views

urlpatterns = [
    path('', views.terminal, name='terminal'),
    path('getMyIP/', views.getMyIP, name='getMyIP'),
    path('genbarcode/', views.genbarcode, name='genbarcode'),
    path('scanphone/', views.scanphone, name='scanphone'),
    path('genqrcode/', views.genqrcode, name='genqrcode')
]