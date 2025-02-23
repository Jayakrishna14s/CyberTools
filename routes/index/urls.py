from django.urls import path, include # type: ignore
from django.contrib import admin # type: ignore
from routes.index import views
urlpatterns = [
    path('', views.index, name='index'),
]