"""rentour URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from users.views import Inicio
from users.views import admin_base
from users.views import *
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Administración Turismo Real"
admin.site.site_title = "RentOur"
admin.site.index_title = "Bienvenidos al Panel"



urlpatterns = [
    path('', Inicio.as_view(), name='index'),
    path('admin_base', admin_base.as_view(), name='admin_base'),
    path('admin/', admin.site.urls),
    path('web/', include(('web.urls', 'web'))),
    path('user/', include(('users.urls', 'users'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)