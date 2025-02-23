from django.urls import path, include # type: ignore
from django.contrib import admin # type: ignore
from routes.subdomain_scanner import views

urlpatterns = [
    path('', views.subdomain_scanner, name='subdomain_scanner'),
    path('scan/', views.scan, name="scan")
]  