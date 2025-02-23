from django.urls import path, include # type: ignore
from django.contrib import admin # type: ignore
from routes.manual import views
\
urlpatterns = [
    path('', views.manual, name='manual'),
]