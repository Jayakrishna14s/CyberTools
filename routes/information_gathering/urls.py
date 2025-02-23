from django.urls import path, include # type: ignore
from django.contrib import admin # type: ignore
from routes.information_gathering import views

urlpatterns = [
    path('', views.information_gathering, name='information_gathering'),
    path("gather/", views.gather, name="gather" )
]