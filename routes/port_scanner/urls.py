from django.urls import path, include # type: ignore
from django.contrib import admin # type: ignore
from routes.port_scanner import views

urlpatterns = [
    path('', views.port_scanner, name='port_scanner'),
    path('scan/', views.scan, name="scan")
]  