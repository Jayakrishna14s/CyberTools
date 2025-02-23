"""
URL configuration for configuration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from django.shortcuts import render

# from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

from django.urls import re_path


from configuration import settings

def custom_404_view(request, exception):
    return render(request, "error.html", status=404)


urlpatterns = [

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('admin/', admin.site.urls),
    path('', include('routes.index.urls')),
    path('informationGathering/', include('routes.information_gathering.urls')),
    path('portScanner/', include('routes.port_scanner.urls')),
    path('subdomainScanner/', include('routes.subdomain_scanner.urls')),
    path('terminal/', include('routes.terminal.urls')),
    path('manual/', include('routes.manual.urls')),    
]

handler404 = 'configuration.urls.custom_404_view'

# if settings.DEBUG:
#     urlpatterns += [
#         path("404/", custom_404_view),
#     ]


